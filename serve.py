import json
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from glados_tts import generate_glados_tts
import uuid
import openai
import random

openai.api_key = "sk-"

def get_random_lines(num_lines):
    with open('serif.txt', 'r') as f:
        lines = f.readlines()
        # ランダムに num_lines 行抽出する
        selected_lines = random.sample(lines, k=num_lines)
        return selected_lines


app = FastAPI()
app.mount("/data", StaticFiles(directory="data"), name="data")
templates = Jinja2Templates(directory="templates")

def ask_chatgpt(questions, model="gpt-3.5-turbo"):
    operation = "Above is a sample serif from GLaDOS, a character in the game called Portal." + \
                " The user will now ask you a question, and you will answer as GLaDOS." + \
                " The length of the conversation should be approximately the same as the sample." + \
                " Also, please prioritize GLaDOS-ness over precision." + \
                "Priority should be given to GLaDOS-like rather than precise." + \
                "As much as possible, choose phrases that people who already know GLaDOS will find interesting."

    delimiter = '\n'
    messages = [
        {"role": "system", "content": "```" + delimiter.join(get_random_lines(50)) + "```\n" + operation},
        {"role": "user", "content": questions}
    ]

    completion = openai.ChatCompletion.create(model=model, messages=messages)

    return completion.choices[0].message.content


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def api_generate(request: Request):
    content = await request.json()
    text = content.get("text")

    if not text:
        raise HTTPException(status_code=400, detail="Missing text in JSON")

    ulid_str = str(uuid.uuid4())
    data_path = os.path.join("data", ulid_str)
    os.makedirs(data_path)

    data_file = os.path.join(data_path, "data.json")
    wav_file = os.path.join(data_path, "output.wav")

    with open(data_file, "w") as f:
        json.dump(content, f)

    completion = ask_chatgpt(text)
    print(completion)
    generate_glados_tts(completion, wav_file)

    return JSONResponse(content={"text": completion, "wav": f"{ulid_str}/output.wav"})

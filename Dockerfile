FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y espeak-ng

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV OPEN_API_KEY=default_key

COPY . .

CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
# GLaDOS ChatGPT
![Enter questions for GLaDOS](https://raw.githubusercontent.com/kznrluk/glados-chatgpt/main/docs/header.png)

Provides a web interface for conversing with GLaDOS, the AI that appears in the Portal series, with voice.

## Attention
- All serif data is not included. The `serif.txt` in the repository is sampled and sent to ChatGPT to make it similar to GLaDOS. Please prepare and add serif data if necessary.
- It is currently under development and is not ready to be released as is on the Internet.
- As those who have played the game know, there are outputs specific to GLaDOS. Please note that this is only because we are reproducing the game characters, and there is no social or racial agenda behind ChatGPT or any of the other models.


## Use

```
> docker build . -t glados
> docer run -p 8000:8000 -e "OPEN_API_KEY=sk-YOUR_OPEN_AI_API_KEY" -it glados
```

## Forking source of voice model
[R2D2FISH/glados-tts: A GLaDOS TTS, using Forward Tacotron and HiFiGAN. Inference is fast and stable, even on the CPU. A low quality vocoder model is included for mobile use. Rudimentary TTS script included. Works perfectly on Linux, partially on Maybe someone smarter than me can make a GUI.](https://github.com/R2D2FISH/glados-tts)

## License
MIT
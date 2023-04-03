import torch
from utils.tools import prepare_text
from scipy.io.wavfile import write

try:
    import winsound
    import os
    os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = 'C:\Program Files\eSpeak NG\libespeak-ng.dll'
    os.environ['PHONEMIZER_ESPEAK_PATH'] = 'C:\Program Files\eSpeak NG\espeak-ng.exe'
except ImportError:
    from subprocess import call

class GLaDOS_TTS:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GLaDOS_TTS, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        print("Initializing TTS Engine...")

        if torch.is_vulkan_available():
            self.device = 'vulkan'
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'

        self.glados = torch.jit.load('models/glados.pt')
        self.vocoder = torch.jit.load('models/vocoder-gpu.pt', map_location=self.device)

        for i in range(2):
            init = self.glados.generate_jit(prepare_text(str(i)))
            init_mel = init['mel_post'].to(self.device)
            init_vo = self.vocoder(init_mel)

    def generate_audio(self, text, output_file):
        x = prepare_text(text).to('cpu')

        with torch.no_grad():
            tts_output = self.glados.generate_jit(x)
            mel = tts_output['mel_post'].to(self.device)
            audio = self.vocoder(mel)

            audio = audio.squeeze()
            audio = audio * 32768.0
            audio = audio.cpu().numpy().astype('int16')

            write(output_file, 22050, audio)


def generate_glados_tts(text, output_file):
    tts_engine = GLaDOS_TTS()
    tts_engine.generate_audio(text, output_file)

import os
import subprocess
import sounddevice as sd
import soundfile as sf
import tempfile


class PiperTTS:

    def __init__(self, piper_bin="piper", voices_dir="voices", voice_file=None):

        self.piper_bin = piper_bin
        self.voices_dir = voices_dir

        # auto-pick first voice if not specified
        if voice_file is None:
            voice_file = self._auto_pick_voice()

        self.voice_path = os.path.join(voices_dir, voice_file)

        if not os.path.exists(self.voice_path):
            raise FileNotFoundError(f"Voice model not found: {self.voice_path}")

        print(f" Piper loaded voice: {voice_file}")

    def _auto_pick_voice(self):

        if not os.path.exists(self.voices_dir):
            raise FileNotFoundError("voices/ folder not found")

        for f in os.listdir(self.voices_dir):
            if f.endswith(".onnx"):
                return f

        raise FileNotFoundError("No .onnx voice models found in voices/")

    def speak(self, text):

        # clean text for better speech flow
        text = self._clean(text)

        sentences = self._split(text)

        for sentence in sentences:

            if not sentence.strip():
                continue

            wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            wav_path = wav_file.name
            wav_file.close()

            try:
                # generate speech
                subprocess.run(
                    [
                        self.piper_bin,
                        "--model", self.voice_path,
                        "--output_file", wav_path
                    ],
                    input=sentence.encode("utf-8"),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False
                )

                # play instantly
                data, fs = sf.read(wav_path, dtype="float32")
                sd.play(data, fs)
                sd.wait()

            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)

    def _split(self, text):
        text = text.replace("!", ".").replace("?", ".")
        return [t.strip() for t in text.split(".") if t.strip()]

    def _clean(self, text):
        # improves natural speech flow
        text = text.replace("\n", " ")
        text = text.replace("*", "")
        return text
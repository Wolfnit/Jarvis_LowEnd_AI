import subprocess
import tempfile
import os


class PiperTTS:


    def __init__(self):

        self.piper_path = "piper"

        self.model = (
            "en_US-amy-medium.onnx"
        )


        print(
            "🟢 Piper TTS ready"
        )



    def speak(self, text):

        if not text:
            return


        wav = tempfile.mktemp(
            suffix=".wav"
        )


        try:

            subprocess.run(
                [
                    self.piper_path,
                    "--model",
                    self.model,
                    "--output_file",
                    wav
                ],
                input=text.encode(),
                check=True
            )


            subprocess.run(
                [
                    "powershell",
                    "-c",
                    f"(New-Object Media.SoundPlayer '{wav}').PlaySync()"
                ]
            )


        except Exception as e:

            print(
                f"❌ Piper error: {e}"
            )


        finally:

            if os.path.exists(wav):

                os.remove(wav)
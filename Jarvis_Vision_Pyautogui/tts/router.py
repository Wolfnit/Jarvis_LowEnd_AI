from tts.pyttsx3_tts import Pyttsx3TTS

try:
    from tts.piper_tts import PiperTTS
except Exception:
    PiperTTS = None


class TTSRouter:

    def __init__(self, mode="auto"):

        self.mode = mode

        self.pyttsx3 = Pyttsx3TTS()

        self.piper = (
            PiperTTS()
            if PiperTTS
            else None
        )

        print(
            f"\n TTS Router initialized in {mode} mode\n"
        )


    def speak(self, text):

        if not text:
            return


        print(
            f" TTS Input: {text}"
        )


        # PYTTSX3 ONLY

        if self.mode == "pyttsx3":

            self.pyttsx3.speak(text)
            return


        # PIPER ONLY

        if self.mode == "piper":

            if self.piper:
                self.piper.speak(text)

            return


        # AUTO

        try:

            self.pyttsx3.speak(text)

        except Exception as e:

            print(
                f" pyttsx3 failed: {e}"
            )

            if self.piper:

                print(
                    " Switching to Piper"
                )

                self.piper.speak(text)
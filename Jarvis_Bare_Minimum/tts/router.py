from tts.pyttsx3_tts import Pyttsx3TTS

# optional Piper
try:
    from tts.piper_tts import PiperTTS
except Exception:
    PiperTTS = None

# Whisper control
from voice import stop_stream, start_stream


class TTSRouter:

    def __init__(self, mode="auto", cloud_tts=None):

        self.mode = mode
        self.pyttsx3 = Pyttsx3TTS()
        self.piper = PiperTTS() if PiperTTS else None
        self.cloud = cloud_tts

        print(f"\n🧠 TTS Router initialized in {mode} mode\n")

    def speak(self, text):

        if not text:
            return

        text = text.strip()

        # stop whisper before speaking
        stop_stream()

        try:

            # FAST MODE (ONLY pyttsx3)
            if self.mode == "fast":
                self.pyttsx3.speak(text)

            # PIPER MODE (ONLY Piper)
            elif self.mode == "piper":
                if self.piper:
                    self.piper.speak(text)
                else:
                    self.pyttsx3.speak(text)

            # CLOUD MODE
            elif self.mode == "cloud":
                if self.cloud:
                    self.cloud.speak(text)
                else:
                    self.pyttsx3.speak(text)

            # AUTO MODE (priority chain)
            else:

                # pyttsx3 FIRST
                try:
                    self.pyttsx3.speak(text)
                    return

                except Exception as e:
                    print(f" pyttsx3 failed: {e}")

                #  Piper SECOND
                if self.piper:
                    try:
                        self.piper.speak(text)
                        print(" Using Piper fallback")
                        return

                    except Exception as e:
                        print(f" Piper failed: {e}")

                # Cloud LAST
                if self.cloud:
                    try:
                        self.cloud.speak(text)
                        print("☁️ Using Cloud fallback")
                        return

                    except Exception as e:
                        print(f"⚠️ Cloud failed: {e}")

                print(" All TTS engines failed")

        finally:
            start_stream()
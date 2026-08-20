import pyttsx3
import threading


class Pyttsx3TTS:

    def __init__(self):

        self.lock = threading.Lock()

        print("\n🟢 pyttsx3 TTS ready\n")


    def create_engine(self):

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            185
        )

        engine.setProperty(
            "volume",
            1.0
        )


        voices = engine.getProperty("voices")

        for voice in voices:

            name = voice.name.lower()

            if (
                "zira" in name
                or "female" in name
                or "aria" in name
            ):
                engine.setProperty(
                    "voice",
                    voice.id
                )
                break


        return engine



    def speak(self, text):

        if not text:
            return


        with self.lock:

            engine = None

            try:

                engine = self.create_engine()

                engine.say(text)

                engine.runAndWait()


            except Exception as e:

                print(
                    f"❌ TTS error: {e}"
                )


            finally:

                if engine:

                    engine.stop()

                    del engine
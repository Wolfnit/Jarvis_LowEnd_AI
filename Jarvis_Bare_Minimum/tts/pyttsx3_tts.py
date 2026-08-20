import pyttsx3


class Pyttsx3TTS:

    def __init__(self):
        self._init_engine()

    def _init_engine(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 185)
        self.engine.setProperty("volume", 1.0)

        voices = self.engine.getProperty("voices")

        selected_voice = None

        print("\n🔍 Loading system voices...\n")

        for v in voices:
            name = v.name.lower()
            print(f"- {v.name}")

            if (
                "zira" in name or
                "aria" in name or
                "female" in name or
                "hazel" in name or
                "susan" in name
            ):
                selected_voice = v.id

        if selected_voice:
            self.engine.setProperty("voice", selected_voice)
            print("\n Female voice selected\n")
        else:
            print("\n Default voice used\n")

    # SAFE SPEAK (NO FREEZE)
    def speak(self, text):

        if not text:
            return

        text = text.replace("\n", " ").strip()

        try:
            # IMPORTANT: reset engine every call
            self.engine.stop()
            self.engine = None

            self._init_engine()

            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as e:
            print(f" TTS error: {e}")
            self._init_engine()
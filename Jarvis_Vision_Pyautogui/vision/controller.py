from vision.capture import capture_screen
from vision.analyzer import VisionAnalyzer


class VisionController:

    def __init__(self, provider):

        self.analyzer = VisionAnalyzer(
            provider
        )


    # ==========================
    # OBSERVE SCREEN
    # ==========================

    def observe(self):

        print(
            "\n👁 Capturing screen..."
        )


        image = capture_screen()


        print(
            "🔎 Analyzing screen..."
        )


        state = self.analyzer.analyze(
            image
        )


        return state
from PIL import Image


class VisionAnalyzer:

    def __init__(self, provider):

        self.provider = provider


    def analyze(self, image_path):

        prompt = """
You are Jarvis vision system.

Analyze the screenshot.

Return ONLY valid JSON:

{
    "summary": "What is visible on screen",
    "errors": [],
    "important": "Important UI elements",
    "task_complete": false,
    "confidence": 0.0
}

Rules:
- Only describe visible information.
- Mention applications, dialogs, buttons, errors, and important text.
- Do not guess.
"""


        result = self.provider.analyze_image(
            image_path,
            prompt
        )


        return result
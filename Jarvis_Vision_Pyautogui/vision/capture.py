import mss
from PIL import Image


def capture_screen():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

    return image


def save_screenshot(path="screen.png"):

    image = capture_screen()

    image.save(path)

    return path
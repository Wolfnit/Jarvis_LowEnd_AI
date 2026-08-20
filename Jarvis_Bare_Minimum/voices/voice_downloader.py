from pathlib import Path
from urllib.request import urlopen

VOICE_DIR = Path(__file__).resolve().parent

BASE_URL = (
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
    "en/en_US/hfc_female/medium/"
)

FILES = [
    "en_US-hfc_female-medium.onnx",
    "en_US-hfc_female-medium.onnx.json",
]


def download(filename):
    destination = VOICE_DIR / filename

    if destination.exists():
        print(f"[OK] {filename} already exists.")
        return

    url = BASE_URL + filename + "?download=true"

    print(f"[DOWNLOAD] {filename}")

    with urlopen(url) as response, open(destination, "wb") as f:
        while chunk := response.read(1024 * 1024):
            f.write(chunk)

    print(f"[OK] Saved: {destination}")


def main():
    print("Downloading Piper voice...")
    
    for filename in FILES:
        download(filename)

    print("\nVoice download complete!")


if __name__ == "__main__":
    main()
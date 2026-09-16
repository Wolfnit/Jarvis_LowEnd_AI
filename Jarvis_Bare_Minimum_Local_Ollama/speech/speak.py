import os
import subprocess
import sounddevice as sd
import soundfile as sf
import tempfile
import urllib.request
import tarfile
import zipfile
import shutil


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PIPER_DIR = os.path.join(
    BASE_DIR,
    "piper"
)

PIPER_EXE = os.path.join(
    PIPER_DIR,
    "piper.exe"
)

VOICE_MODEL = os.path.join(
    PIPER_DIR,
    "en_US-kristin-medium.onnx"
)

VOICE_CONFIG = os.path.join(
    PIPER_DIR,
    "en_US-kristin-medium.onnx.json"
)

ESPEAK_DATA = os.path.join(
    PIPER_DIR,
    "espeak-ng-data"
)


# ============================================================
# DOWNLOAD URLs
# ============================================================

PIPER_URL = (
    "https://github.com/rhasspy/piper/releases/download/"
    "2023.11.14-2/piper_windows_amd64.zip"
)

ESPEAK_DATA_URL = (
    "https://github.com/rhasspy/piper/releases/download/"
    "2023.11.14-2/piper_linux_x86_64.tar.gz"
)

VOICE_URL = (
    "https://huggingface.co/rhasspy/piper-voices/"
    "resolve/main/en/en_US/kristin/medium/"
    "en_US-kristin-medium.onnx"
)

VOICE_CONFIG_URL = (
    "https://huggingface.co/rhasspy/piper-voices/"
    "resolve/main/en/en_US/kristin/medium/"
    "en_US-kristin-medium.onnx.json"
)


# ============================================================
# DOWNLOAD
# ============================================================

def download(url, destination):

    print(
        f"[Piper] Downloading "
        f"{os.path.basename(destination)}..."
    )

    urllib.request.urlretrieve(
        url,
        destination
    )


# ============================================================
# PIPER PACKAGE
# ============================================================

def setup_piper_binary():

    required = [
        "piper.exe",
        "espeak-ng.dll",
        "piper_phonemize.dll",
        "onnxruntime.dll",
    ]

    if all(
        os.path.exists(
            os.path.join(PIPER_DIR, file)
        )
        for file in required
    ):
        return

    print("[Piper] Piper package missing.")
    print("[Piper] Downloading Piper...")

    archive = os.path.join(
        BASE_DIR,
        "_piper_windows.zip"
    )

    extract_dir = os.path.join(
        BASE_DIR,
        "_piper_extract"
    )

    try:

        download(
            PIPER_URL,
            archive
        )

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

        os.makedirs(
            extract_dir
        )

        with zipfile.ZipFile(
            archive,
            "r"
        ) as z:

            z.extractall(
                extract_dir
            )

        for file in required:

            source = None

            for root, dirs, files in os.walk(
                extract_dir
            ):

                if file in files:

                    source = os.path.join(
                        root,
                        file
                    )

                    break

            if source:

                shutil.copy2(
                    source,
                    os.path.join(
                        PIPER_DIR,
                        file
                    )
                )

        shutil.rmtree(
            extract_dir,
            ignore_errors=True
        )

        os.remove(
            archive
        )

    except Exception:

        if os.path.exists(archive):
            os.remove(archive)

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

        raise


# ============================================================
# eSPEAK DATA
# ============================================================

def setup_espeak():

    phontab = os.path.join(
        ESPEAK_DATA,
        "phontab"
    )

    if os.path.exists(phontab):
        return

    print("[Piper] eSpeak-ng data missing.")
    print("[Piper] Downloading eSpeak-ng data...")

    archive = os.path.join(
        BASE_DIR,
        "_piper_data.tar.gz"
    )

    extract_dir = os.path.join(
        BASE_DIR,
        "_piper_data_extract"
    )

    try:

        download(
            ESPEAK_DATA_URL,
            archive
        )

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

        os.makedirs(
            extract_dir
        )

        with tarfile.open(
            archive,
            "r:gz"
        ) as tar:

            tar.extractall(
                extract_dir,
                filter="data"
            )

        # Search for the actual espeak-ng-data directory
        found = None

        for root, dirs, files in os.walk(
            extract_dir
        ):

            if (
                "phontab" in files
                and "phondata" in files
            ):

                found = root
                break

        if found is None:

            raise RuntimeError(
                "Downloaded Piper archive does not "
                "contain a valid espeak-ng-data directory."
            )

        if os.path.exists(
            ESPEAK_DATA
        ):

            shutil.rmtree(
                ESPEAK_DATA
            )

        shutil.copytree(
            found,
            ESPEAK_DATA
        )

        shutil.rmtree(
            extract_dir,
            ignore_errors=True
        )

        os.remove(
            archive
        )

    except Exception:

        if os.path.exists(archive):
            os.remove(archive)

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

        raise


# ============================================================
# VOICE
# ============================================================

def setup_voice():

    if not os.path.exists(
        VOICE_MODEL
    ):

        download(
            VOICE_URL,
            VOICE_MODEL
        )

    if not os.path.exists(
        VOICE_CONFIG
    ):

        download(
            VOICE_CONFIG_URL,
            VOICE_CONFIG
        )


# ============================================================
# INITIALIZE EVERYTHING
# ============================================================

os.makedirs(
    PIPER_DIR,
    exist_ok=True
)

setup_piper_binary()
setup_espeak()
setup_voice()

print(
    "Piper loaded: en_US-kristin-medium"
)


# ============================================================
# SPEAK
# ============================================================

def speak(text):

    if not text:
        return

    text = text.replace(
        "\n",
        " "
    )

    text = text.replace(
        "*",
        ""
    )

    text = " ".join(
        text.split()
    )

    if not text:
        return

    wav_path = None

    try:

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        wav_path = temp.name
        temp.close()

        result = subprocess.run(
            [
                PIPER_EXE,

                "--model",
                VOICE_MODEL,

                "--config",
                VOICE_CONFIG,

                "--espeak_data",
                ESPEAK_DATA,

                # Faster speech
                "--length_scale",
                "0.8",

                # Very short punctuation pause
                "--sentence_silence",
                "0.05",

                "--output_file",
                wav_path
            ],

            input=text.encode(
                "utf-8"
            ),

            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,

            check=False
        )

        if result.returncode != 0:

            print("[Piper Error]")

            print(
                result.stderr.decode(
                    "utf-8",
                    errors="replace"
                )
            )

            return

        audio, sample_rate = sf.read(
            wav_path,
            dtype="float32"
        )

        sd.play(
            audio,
            samplerate=sample_rate
        )

        sd.wait()

    except Exception as e:

        print(
            f"[Speech Error] {e}"
        )

    finally:

        if (
            wav_path
            and os.path.exists(wav_path)
        ):

            try:
                os.remove(
                    wav_path
                )

            except OSError:
                pass
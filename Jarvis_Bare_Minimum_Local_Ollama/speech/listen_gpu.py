import os
import queue
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import sounddevice as sd
import sherpa_onnx


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "sherpa-onnx-streaming-zipformer-en-2023-06-26"

MODEL_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/"
    "asr-models/"
    f"{MODEL_NAME}.tar.bz2"
)

MODEL_ARCHIVE = MODEL_DIR / f"{MODEL_NAME}.tar.bz2"
MODEL_FOLDER = MODEL_DIR / MODEL_NAME


# ============================================================
# AUDIO
# ============================================================

SAMPLE_RATE = 16000
BLOCK_SIZE = 1600

audio_queue = queue.Queue()

stream = None


# ============================================================
# FIND MODEL FILES
# ============================================================

def find_model_file(name):

    for path in MODEL_FOLDER.rglob("*"):

        if path.is_file() and name in path.name:
            return path

    return None


# ============================================================
# DOWNLOAD + EXTRACT MODEL
# ============================================================

def setup_model():

    tokens = find_model_file("tokens.txt")

    if tokens is not None:
        return

    print("[Speech] Streaming model not found.")
    print("[Speech] Downloading model...")
    print("[Speech] This only happens once.\n")

    if not MODEL_ARCHIVE.exists():

        urllib.request.urlretrieve(
            MODEL_URL,
            MODEL_ARCHIVE
        )

    print("\n[Speech] Extracting model...")

    with tarfile.open(
        MODEL_ARCHIVE,
        "r:bz2"
    ) as archive:

        archive.extractall(
            MODEL_DIR,
            filter="data"
        )

    print("[Speech] Model downloaded.\n")


# ============================================================
# LOAD MODEL
# ============================================================

setup_model()

print("[Speech] Loading streaming ASR...")

tokens = find_model_file("tokens.txt")
encoder = find_model_file("encoder-")
decoder = find_model_file("decoder-")
joiner = find_model_file("joiner-")


if not tokens:
    raise RuntimeError("tokens.txt not found.")

if not encoder:
    raise RuntimeError("Encoder model not found.")

if not decoder:
    raise RuntimeError("Decoder model not found.")

if not joiner:
    raise RuntimeError("Joiner model not found.")


print(
    f"[Speech] Encoder: {encoder.name}"
)

print(
    f"[Speech] Decoder: {decoder.name}"
)

print(
    f"[Speech] Joiner:  {joiner.name}"
)


recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(

    tokens=str(tokens),

    encoder=str(encoder),

    decoder=str(decoder),

    joiner=str(joiner),

    num_threads=4,

    decoding_method="greedy_search",

    enable_endpoint_detection=True,

    rule1_min_trailing_silence=0.7,

    rule2_min_trailing_silence=1.0,

    rule3_min_utterance_length=0.5
)


print("[Speech] Streaming ASR ready.\n")


# ============================================================
# AUDIO CALLBACK
# ============================================================

def callback(
    indata,
    frames,
    time_info,
    status
):

    if status:
        pass

    audio_queue.put(
        indata[:, 0].copy()
    )


# ============================================================
# START MICROPHONE
# ============================================================

def start_stream():

    global stream

    if stream is not None:
        return

    stream = sd.InputStream(

        samplerate=SAMPLE_RATE,

        channels=1,

        dtype="float32",

        blocksize=BLOCK_SIZE,

        callback=callback
    )

    stream.start()


# ============================================================
# STOP MICROPHONE
# ============================================================

def stop_stream():

    global stream

    if stream is not None:

        stream.stop()
        stream.close()

        stream = None

    while not audio_queue.empty():

        try:
            audio_queue.get_nowait()

        except queue.Empty:
            break


# ============================================================
# LISTEN
# ============================================================

def listen_once():

    start_stream()

    recognizer_stream = recognizer.create_stream()

    while True:

        samples = audio_queue.get()

        recognizer_stream.accept_waveform(
            SAMPLE_RATE,
            samples
        )

        while recognizer.is_ready(
            recognizer_stream
        ):

            recognizer.decode_stream(
                recognizer_stream
            )

        # ----------------------------------------------------
        # ENDPOINT DETECTED
        # ----------------------------------------------------

        if recognizer.is_endpoint(
            recognizer_stream
        ):

            result = recognizer.get_result(
                recognizer_stream
            )

            text = result.strip()

            recognizer.reset(
                recognizer_stream
            )

            if text:
                return text
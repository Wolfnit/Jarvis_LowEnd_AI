import queue
import time
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# ==========================
# SETTINGS
# ==========================

SAMPLE_RATE = 16000
BLOCK_SIZE = 1600
SILENCE_TIME = 1.0

# ==========================
# LOAD WHISPER
# ==========================

print("Loading Whisper...")

model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)

# ==========================
# CALIBRATE MIC
# ==========================

print("Calibrating microphone... Stay quiet for 3 seconds.")

noise_samples = []

for _ in range(30):

    audio = sd.rec(
        BLOCK_SIZE,
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    rms = np.sqrt(np.mean(audio.flatten() ** 2))
    noise_samples.append(rms)

noise_floor = np.mean(noise_samples)
THRESHOLD = noise_floor * 3

print(f"Noise Floor: {noise_floor:.5f}")
print(f"Threshold:   {THRESHOLD:.5f}")
print("Ready.\n")

# ==========================
# AUDIO SYSTEM STATE
# ==========================

audio_queue = queue.Queue()
stream = None   # 🔥 IMPORTANT GLOBAL STREAM HANDLE

# ==========================
# CALLBACK
# ==========================

def callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())

# ==========================
# STREAM CONTROL
# ==========================

def start_stream():
    global stream

    if stream:
        return

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=BLOCK_SIZE,
        callback=callback
    )
    stream.start()


def stop_stream():
    global stream

    if stream:
        stream.stop()
        stream.close()
        stream = None

    # clear leftover audio
    while not audio_queue.empty():
        audio_queue.get()

# ==========================
# DUPLICATE PROTECTION
# ==========================

_last_return_time = 0

# ==========================
# LISTEN FUNCTION
# ==========================

def listen_once():

    global _last_return_time

    recording = False
    speech_buffer = []
    silence_counter = 0

    # ensure stream is running
    start_stream()

    while True:

        chunk = audio_queue.get().flatten()

        rms = np.sqrt(np.mean(chunk ** 2))

        if rms > THRESHOLD:

            if not recording:
                recording = True
                speech_buffer = []

            speech_buffer.append(chunk)
            silence_counter = 0

        elif recording:

            speech_buffer.append(chunk)
            silence_counter += 1

            silence_seconds = (silence_counter * BLOCK_SIZE) / SAMPLE_RATE

            if silence_seconds >= SILENCE_TIME:

                audio = np.concatenate(speech_buffer)

                segments, _ = model.transcribe(
                    audio,
                    beam_size=1
                )

                text = " ".join(
                    seg.text.strip()
                    for seg in segments
                ).strip()

                # flush queue
                while not audio_queue.empty():
                    audio_queue.get()

                now = time.time()

                if now - _last_return_time < 1.5:
                    recording = False
                    speech_buffer = []
                    silence_counter = 0
                    continue

                _last_return_time = now

                recording = False
                speech_buffer = []
                silence_counter = 0

                if text:
                    return text
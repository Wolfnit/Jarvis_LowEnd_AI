# 🟢 Jarvis — Bare Minimum

> The first public version of Jarvis: a simple AI voice assistant for Windows.

This version focuses on the basic **voice → AI → voice** pipeline before moving toward computer control, vision, memory, and autonomy.

---

## 🎯 What Does It Do?

Jarvis listens to your voice, converts it to text using **Whisper**, sends it to an AI provider, and speaks the response using TTS.

```text
🎙️ Microphone
      ↓
🗣️ Whisper
      ↓
🧠 AI Provider
      ↓
📝 AI Response
      ↓
🔊 TTS Router
   ↙       ↘
Piper    pyttsx3
      ↓
🔈 Speaker
```

---

## ✨ Features

- 🎙️ Voice input
- 🗣️ Whisper speech recognition
- 🧠 AI-generated responses
- 🔊 Piper TTS
- 🗣️ pyttsx3 TTS
- 🔌 Modular AI providers
- 🔀 TTS routing
- 🪶 Designed for low-end hardware
- 🪟 Windows-focused

---

## 🧠 Voice Detection

One of the main challenges was deciding **when Jarvis should record**.

A microphone constantly receives sound, so Jarvis uses a **noise threshold** to distinguish speech from background noise.

```text
Audio Level

High ─────────────────
     │    SPEECH      │
     │   ████████     │
     │   ████████     │
─────┼────────────────┼── Noise threshold
     │ Background     │
Low  ─────────────────
```

A threshold that is too low can cause background noise to trigger recording, while a threshold that is too high can cause quiet speech to be missed.

This is an early approach to **Voice Activity Detection (VAD)**. Future versions can use more robust VAD and wake-word detection.

> The challenge isn't only *"How do I convert speech to text?"* — it's also **"How does Jarvis know when I'm actually talking to it?"**

---

## 📁 Project Structure

```text
Jarvis_Bare_Minimum/
├── providers/
│   ├── gemini_provider.py
│   └── router.py
├── tts/
│   ├── cloud_tts.py
│   ├── piper_tts.py
│   ├── pyttsx3_tts.py
│   └── router.py
├── voices/
│   └── voice_downloader.py
├── jarvis.py
├── voice.py
├── Requirements.txt
└── .gitignore
```

### Main Components

- `jarvis.py` — Main application and control flow.
- `voice.py` — Voice input and speech processing.
- `providers/` — AI provider system.
- `tts/` — Text-to-speech system and routing.
- `voices/` — Piper voice downloader.

The actual Piper voice model is **not included** in the repository.

---

## ⚙️ Requirements

- Windows
- Python 3
- Microphone
- Speakers/headphones
- Internet connection for the configured AI provider

---

## 🚀 Installation

### 1. Enter the folder

```bash
cd Jarvis_Bare_Minimum
```

### 2. Install dependencies

```bash
pip install -r Requirements.txt
```

### 3. Download the Piper voice

```bash
python voices/voice_downloader.py
```

### 4. Configure your AI provider

Configure the required API credentials according to the provider implementation.

**Never commit API keys or other secrets to GitHub.**

### 5. Run Jarvis

```bash
python jarvis.py
```


---

## ⚠️ Current Limitations

This is intentionally a **bare-minimum** version.

Currently it does not include:

- ❌ Computer vision
- ❌ Mouse/keyboard control
- ❌ Memory bugged for long facts
- ❌ Autonomous task planning
- ❌ Full computer control
- ❌ AI operating-system integration

---

## 🔮 What's Next?

The long-term direction is:

```text
Voice Assistant
      ↓
Tools
      ↓
Vision
      ↓
Memory
      ↓
Autonomous Tasks
      ↓
AI Operating System
```

This is **Version 01** of the larger Jarvis project.

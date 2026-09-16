# 🟢 Jarvis — Bare Minimum Local Ollama

> A minimal local AI voice assistant for Windows powered by Ollama.

```text
🎙️ Microphone
      ↓
🗣️ Speech Recognition
      ↓
🧠 Ollama
      ↓
💬 Response
      ↓
🔊 Piper
      ↓
🔈 Speaker
```

## ✨ Features

* 🎙️ CPU / GPU speech recognition
* ⚡ Streaming speech with Sherpa-ONNX
* 🧠 Local Ollama models
* 🔀 User-selectable AI model
* 🔊 Piper TTS
* 📦 Automatic Piper setup
* 🧠 Short-term + long-term memory
* 🪟 Windows focused

## 📁 Structure

```text
Jarvis_Bare_Minimum_Local_Ollama/
├── brain/
│   └── brain.py
├── memory/
│   └── memory.py
├── speech/
│   ├── listen_cpu.py
│   ├── listen_gpu.py
│   └── speak.py
├── piper/
├── jarvis.py
├── Requirements.txt
└── .gitignore
```

## 🚀 Run

```bash
pip install -r Requirements.txt
python jarvis.py
```

Jarvis automatically detects installed Ollama models and lets you choose the AI and speech engine.

## 🔮 Roadmap

```text
Voice
 ↓
Tools
 ↓
Computer Control
 ↓
Vision
 ↓
Memory
 ↓
Autonomous Agent
```

**Jarvis V0.1 — Building a local AI assistant from the ground up.**

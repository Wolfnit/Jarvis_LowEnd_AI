# 🟡 Jarvis — Windows Vision

> The second stage of Jarvis: a voice-controlled AI assistant with computer vision and GUI control.

This version builds on the **Bare Minimum** voice assistant and introduces:

* 🎙️ Voice commands using Whisper
* 🧠 AI planning using Gemini
* 🖥️ Windows GUI control using PyAutoGUI
* 👁️ Screen capture and vision analysis
* 🔎 Task verification
* 🔁 Basic recovery actions
* 🔊 Piper / pyttsx3 TTS
* 🧠 Experimental memory system

## 🔄 How It Works

```text
Voice
  ↓
Whisper
  ↓
AI Planner
  ↓
GUI Action
  ↓
Screen Capture
  ↓
Vision
  ↓
Verifier
  ↓
Complete / Recover
```

The main goal is to experiment with an AI that can **perform an action, look at the screen, and check whether it actually worked.**

## ⚠️ Important

This version has **not been thoroughly bug-tested** yet.

Some actions, vision results, or verification decisions may not work correctly.

**Sorry for any inconvenience!**

If you try it, please share your **feedback, your versions of the project, and suggestions**. They will help improve future versions of Jarvis.

## 🚀 Installation

Install the required packages:

```bash
pip install -r Requirements.txt
```

Configure your Gemini API credentials, then run:

```bash
python Jarvis.py
```

## 🐺 What's Next?

Future versions will focus on:

* Better screen understanding
* More reliable mouse control
* Better task verification
* Smarter recovery
* Memory
* More autonomous computer control
* Eventually, an AI-powered operating system

---

❤️ **Thanks for checking out Jarvis!**

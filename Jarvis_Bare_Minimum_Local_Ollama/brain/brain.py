import ollama


# MODEL IS SELECTED BY jarvis.py
MODEL = None


SYSTEM_PROMPT = """You are Jarvis, a personal voice assistant.

Your personality:
- Calm
- Intelligent
- Natural
- Helpful
- Concise

You have two types of memory:

1. SHORT-TERM MEMORY
Recent conversation history. Use it to understand the current conversation.

2. LONG-TERM MEMORY
Important facts saved about the user. Use these facts when relevant.

Return your answer as JSON with exactly these fields:

{
    "response": "What Jarvis should say to the user",
    "memory": [
        "Important long-term fact worth remembering"
    ]
}

Rules:
- "response" will be spoken aloud.
- Keep responses short and natural.
- Usually 1-3 sentences.
- Do not use markdown or emojis.
- Only put genuinely useful long-term user facts in "memory".
- Do not save temporary information, greetings, questions, or normal conversation.
- Do not guess facts.
- If there is nothing worth remembering, use an empty memory list.
"""


def set_model(model):
    global MODEL
    MODEL = model


def think(user_text, short_term_memory="", long_term_memory=""):

    if not MODEL:
        raise RuntimeError("No Ollama model selected.")

    prompt = f"""\
{SYSTEM_PROMPT}

=== SHORT-TERM MEMORY ===
{short_term_memory}

=== LONG-TERM MEMORY ===
{long_term_memory}

=== CURRENT USER MESSAGE ===
{user_text}

Use the memories when relevant.
"""

    result = ollama.chat(
        model=MODEL,
        think=False,
        format="json",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.4
        }
    )

    return result["message"]["content"]
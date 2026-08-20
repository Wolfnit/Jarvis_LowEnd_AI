import os
import json
import sqlite3
from datetime import datetime

from voice import listen_once
from providers.router import create_provider

from tts.router import TTSRouter

CONFIG_FILE = "config.json"
MEMORY_DB = "memory.db"


# CONFIG

def setup_config():

    print("\n" + "=" * 40)
    print("          JARVIS SETUP")
    print("=" * 40)

    print("\nProviders:")
    print("1. Gemini")

    input("\nSelect Provider [1]: ")

    provider = "gemini"

    api_key = input("\nGemini API Key: ").strip()

    model = input(
        "\nModel [models/gemini-2.5-flash]: "
    ).strip()

    if not model:
        model = "models/gemini-2.5-flash"

    username = input("\nYour Name: ").strip()

    assistant_name = input(
        "\nAssistant Name [Jarvis]: "
    ).strip()

    if not assistant_name:
        assistant_name = "Jarvis"

    config = {
        "provider": provider,
        "api_key": api_key,
        "model": model,
        "username": username,
        "assistant_name": assistant_name
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print("\n Config saved.\n")

    return config


def load_config():

    if not os.path.exists(CONFIG_FILE):
        return setup_config()

    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    except Exception:
        print("⚠️ Config corrupted.")
        return setup_config()


# MEMORY

def init_memory():

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        role TEXT,
        message TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS facts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


def save_memory(role, message):

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO conversations
        (timestamp, role, message)
        VALUES (?, ?, ?)
    """, (
        datetime.now().isoformat(),
        role,
        message
    ))

    conn.commit()
    conn.close()


def get_recent_memory(limit=15):

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT role, message
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return list(reversed(rows))


def save_fact(fact):

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO facts(fact)
        VALUES(?)
    """, (fact,))

    conn.commit()
    conn.close()


def get_facts():

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("SELECT fact FROM facts")

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]


def extract_facts(text):

    t = text.lower()

    if "my name is" in t:
        name = text.split("my name is", 1)[-1].strip()
        if name:
            save_fact(f"User's name is {name}")

    if "i like" in t:
        item = text.split("i like", 1)[-1].strip()
        if item:
            save_fact(f"User likes {item}")

    if "i want to" in t:
        goal = text.split("i want to", 1)[-1].strip()
        if goal:
            save_fact(f"User wants to {goal}")


def clear_memory():

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM conversations")
    cur.execute("DELETE FROM facts")

    conn.commit()
    conn.close()

    print("🗑 Memory cleared.\n")


# STARTUP

config = load_config()
init_memory()

provider = create_provider(
    config["provider"],
    config["api_key"],
    config["model"]
)

assistant_name = config["assistant_name"]
username = config["username"]

from tts.router import TTSRouter

tts = TTSRouter(mode="auto")

print("\n" + "=" * 40)
print(f" {assistant_name} Online")
print("=" * 40)

print(f"\nHello {username}.\n")

print("Commands:")
print("  /config  -> reconfigure")
print("  /memory  -> show facts")
print("  /clear   -> clear memory")
print("  /exit    -> quit")
print("\nSpeak naturally...\n")


# MAIN LOOP

while True:

    try:

        text = listen_once()

        if not text:
            continue

        print(f"\nYOU: {text}")

        command = text.lower().strip()

        if command == "/exit":
            print(f"\n{assistant_name}: Goodbye!")
            break

        if command in ["/clear", "clear"]:
            clear_memory()
            continue

        if command in ["/memory", "memory"]:

            facts = get_facts()

            print("\n===== FACTS =====\n")

            if not facts:
                print("No facts stored.\n")

            for f in facts:
                print("-", f)

            print()
            continue

        if command == "/config":
            config = setup_config()

            provider = create_provider(
                config["provider"],
                config["api_key"],
                config["model"]
            )

            assistant_name = config["assistant_name"]
            username = config["username"]

            print("\n🔄 Configuration reloaded.\n")
            continue

        # SAVE USER MESSAGE
        save_memory("user", text)

        # EXTRACT FACTS
        extract_facts(text)

        # BUILD MEMORY CONTEXT
        facts = get_facts()
        recent = get_recent_memory()

        fact_block = "\n".join(f"- {f}" for f in facts)

        conversation_block = "\n".join(
            f"{r}: {m}" for r, m in recent
        )

        prompt = f"""
You are {assistant_name}.
You are users humorus best friend.
You reply in single lines, during normal convos.
Known facts about the user:
{fact_block}

Recent conversation:
{conversation_block}

User message:
{text}

Use memory when relevant.
Respond naturally.
"""

        response = provider.generate(prompt)

        print(f"\n{assistant_name}: {response}\n")

        tts.speak(response)
        
        save_memory("assistant", response)

    except KeyboardInterrupt:
        print(f"\n\n{assistant_name}: Shutting down...")
        break

    except Exception as e:
        print(f"\n Error: {e}\n")
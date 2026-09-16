import sqlite3
from pathlib import Path

# DATABASE PATHS

BASE_DIR = Path(__file__).resolve().parent

SHORT_TERM_DB = BASE_DIR / "short_term.db"
LONG_TERM_DB = BASE_DIR / "long_term.db"

MAX_TURNS = 10


# INITIALIZE DATABASES

def init_databases():

    # Short-term memory
    with sqlite3.connect(SHORT_TERM_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                jarvis TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # Long-term memory
    with sqlite3.connect(LONG_TERM_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT UNIQUE NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


# SHORT-TERM MEMORY

def add_conversation(user_text, jarvis_response):

    with sqlite3.connect(SHORT_TERM_DB) as conn:

        conn.execute(
            """
            INSERT INTO conversations (user, jarvis)
            VALUES (?, ?)
            """,
            (user_text, jarvis_response)
        )

        # Keep only the newest 10 turns
        conn.execute("""
            DELETE FROM conversations
            WHERE id NOT IN (
                SELECT id
                FROM conversations
                ORDER BY id DESC
                LIMIT ?
            )
        """, (MAX_TURNS,))


def get_short_term():

    with sqlite3.connect(SHORT_TERM_DB) as conn:

        rows = conn.execute("""
            SELECT user, jarvis
            FROM conversations
            ORDER BY id ASC
        """).fetchall()

    conversation = []

    for user, jarvis in rows:
        conversation.append(f"User: {user}")
        conversation.append(f"Jarvis: {jarvis}")

    return "\n".join(conversation)


# LONG-TERM MEMORY

def add_facts(facts):

    if not facts:
        return

    with sqlite3.connect(LONG_TERM_DB) as conn:

        for fact in facts:

            fact = str(fact).strip()

            if not fact:
                continue

            conn.execute(
                """
                INSERT OR IGNORE INTO facts (fact)
                VALUES (?)
                """,
                (fact,)
            )


def get_long_term():

    with sqlite3.connect(LONG_TERM_DB) as conn:

        rows = conn.execute("""
            SELECT fact
            FROM facts
            ORDER BY id ASC
        """).fetchall()

    return "\n".join(
        f"- {fact}"
        for (fact,) in rows
    )


init_databases()
import sqlite3


class Memory:

    def __init__(self, db_file="memory.db"):

        self.db_file = db_file

        self.init()

    # =====================================
    # INITIALIZE DATABASE
    # =====================================

    def init(self):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # =====================================
    # CONVERSATION
    # =====================================

    def save_message(self, role, message):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO conversations(role, message)
            VALUES (?, ?)
            """,
            (role, message)
        )

        conn.commit()
        conn.close()

    def get_recent(self, limit=10):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role, message
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cur.fetchall()

        conn.close()

        return list(reversed(rows))

    # =====================================
    # LONG TERM MEMORY
    # =====================================

    def save_fact(self, fact):

        if not fact:
            return

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT OR IGNORE INTO facts(fact)
            VALUES (?)
            """,
            (fact,)
        )

        conn.commit()
        conn.close()

    def get_facts(self):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT fact
            FROM facts
            """
        )

        rows = cur.fetchall()

        conn.close()

        return [row[0] for row in rows]

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute("DELETE FROM conversations")
        cur.execute("DELETE FROM facts")

        conn.commit()
        conn.close()
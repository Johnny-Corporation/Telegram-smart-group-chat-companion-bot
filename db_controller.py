import sqlite3
from os import path


class Controller:
    def __init__(self, db_name: str = "MessageEvents") -> None:
        self.sqlite_name = db_name
        if not path.exists(f"{db_name}.sqlite"):
            self._create_db()
        self.conn = sqlite3.connect(f"{db_name}.sqlite", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def _create_db(self):
        conn = sqlite3.connect(f"{self.sqlite_name}.sqlite", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE MessageEvents (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ChatID INTEGER,
                MessageText TEXT,
                Time TEXT,
                SenderFirstName TEXT,
                SenderLastName TEXT,
                SenderUsername TEXT,
                TokensTotal INTEGER
            )
        """
        )

        conn.commit()
        cursor.close()
        conn.close()

    def add_message_event(
        self,
        chat_id,
        text,
        time,
        first_name,
        last_name,
        username,
        tokens_total=None,
    ):
        self.cursor.execute(
            f"""
            INSERT INTO MessageEvents (ChatID, MessageText, Time, SenderFirstName, SenderLastName, SenderUsername, TokensTotal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                text,
                time,
                first_name,
                last_name,
                username,
                tokens_total,
            ),
        )
        self.conn.commit()

    def get_last_n_message_events_from_chat(self, n, chat_id=None):
        self.cursor.execute(
            f"""
            SELECT * FROM MessageEvents
            {"WHERE ChatID = ?" if chat_id else ""}
            ORDER BY Time DESC
            LIMIT ?
            """,
            ((n, chat_id) if chat_id else (n,)),
        )
        return self.cursor.fetchall()

    def get_last_n_messages_from_chat(self, n, chat_id=None):
        message_events = self.get_last_n_message_events_from_chat(n, chat_id)

        # Extract the text of the messages
        messages = [event[2] for event in message_events]

        return messages

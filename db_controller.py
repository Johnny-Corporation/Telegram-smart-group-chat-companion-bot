import sqlite3
from os import path


class Controller:
    """Controls all operations with sqlite database"""

    def __init__(self, db_name: str = "MessageEvents") -> None:
        """Creates db if it doesn't exist, connects to db
        Args:
            db_name (str, optional) Defaults to "MessageEvents".
        """
        self.sqlite_name = db_name
        if not path.exists(f"{db_name}.sqlite"):
            self._create_db()
        self.conn = sqlite3.connect(f"{db_name}.sqlite", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def _create_db(self) -> None:
        """Private method, used to create and init db"""
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
                PromptTokensTotal INTEGER,
                CompletionTokensTotal INTEGER
            )
        """
        )

        conn.commit()
        cursor.close()
        conn.close()

    def add_message_event(
        self,
        chat_id: int,
        text: str,
        time: str,
        first_name: str,
        last_name: str,
        username: str,
        prompt_tokens_total: int,
        completion_tokens_total: int,
    ):
        """Adds new row to db

        Args:
            chat_id (int)
            text (str)
            time (str): format HH:mm:ss.SSSSSSS (%Y-%m-%d %H:%M:%S.%f)
            first_name (str)
            last_name (str)
            username (str)
            prompt_tokens_total (int, optional): Total amount of prompt tokens spent in this chat. Only for GPT messages. Defaults to None.
            completion_tokens_total (int, optional): Total amount of completion tokens spent in this chat. Only for GPT messages. Defaults to None.
        """
        self.cursor.execute(
            f"""
            INSERT INTO MessageEvents (ChatID, MessageText, Time, SenderFirstName, SenderLastName, SenderUsername, PromptTokensTotal, CompletionTokensTotal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                text,
                time,
                first_name,
                last_name,
                username,
                prompt_tokens_total,
                completion_tokens_total,
            ),
        )
        self.conn.commit()

    def get_last_n_message_events_from_chat(self, n: int, chat_id: int = None):
        """Get last n rows from db in list format

        Args:
            n (int): number of rows
            chat_id (int, optional): If set, returns n last rows with specified id. Defaults to None.

        Returns:
            list
        """
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

    def get_last_n_messages_from_chat(self, n: int, chat_id: int = None):
        """Get last n messages from db

        Args:
            n (int): number of messages
            chat_id (int, optional): Chat id. Defaults to None. If not set returns messages from all chats

        Returns:
            list
        """
        message_events = self.get_last_n_message_events_from_chat(n, chat_id)

        # Extract the text and names from events
        messages = [[event[4], event[2]] for event in message_events]

        return messages

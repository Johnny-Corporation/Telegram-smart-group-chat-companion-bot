import sqlite3
from os import path


class Controller:
    """Controls all operations with sqlite database"""

    def __init__(self, db_name: str = "DB") -> None:
        """Creates db if it doesn't exist, connects to db
        Args:
            db_name (str, optional) Defaults to "MessageEvents".
        """
        self.sqlite_name = db_name
        if not path.exists(f"output\\{db_name}.sqlite"):
            self._create_db()
        self.conn = sqlite3.connect(
            f"output\\{db_name}.sqlite", check_same_thread=False
        )
        self.cursor = self.conn.cursor()

    def _create_db(self) -> None:
        """Private method, used to create and init db"""
        conn = sqlite3.connect(
            f"output\\{self.sqlite_name}.sqlite", check_same_thread=False
        )
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
                SenderUsername TEXT
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE UserSubscriptions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ChatID INTEGER,
                GroupChatIDs TEXT,
                SenderFirstName TEXT,
                SenderLastName TEXT,
                SenderUsername TEXT
            )
        """
        )

        conn.commit()
        cursor.close()
        conn.close()

    def add_user_with_sub(
        self,
        chat_id: int,
        group_chat_ids: str,
        sender_first_name: str,
        sender_last_name: str,
        sender_username: str,
        dynamic_generation: bool,
        voice_input: bool,
        voice_output: bool,
    ) -> None:
        sql = """
            INSERT INTO UserSubscriptions (
                ChatID,
                GroupChatIDs,
                SenderFirstName,
                SenderLastName,
                SenderUsername,
                DYNAMIC_GENERATION,
            ) VALUES (?, ?, ?, ?, ?, ?)
        """

        self.cursor.execute(
            sql,
            (
                chat_id,
                group_chat_ids,
                sender_first_name,
                sender_last_name,
                sender_username,
                int(dynamic_generation),
                int(voice_input),
                int(voice_output),
            ),
        )

        self.conn.commit()

    def add_message_event(
        self,
        chat_id: int,
        text: str,
        time: str,
        first_name: str,
        last_name: str,
        username: str,
    ):
        self.cursor.execute(
            f"""
            INSERT INTO MessageEvents (ChatID, MessageText, Time, SenderFirstName, SenderLastName, SenderUsername)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                text,
                time,
                first_name,
                last_name,
                username,
            ),
        )
        self.conn.commit()

    def get_user_with_sub_by_chat_id(self, user_chat_id: int) -> dict:
        """Returns dict with data about user where each key is a column name"""
        query = "SELECT * FROM UserSubscriptions WHERE ChatID = ?"
        self.cursor.execute(query, (user_chat_id,))
        result = self.cursor.fetchone()

        if result is None:
            return {}  # User not found

        # Convert the row into a dictionary
        columns = [description[0] for description in self.cursor.description]
        users_dict = {}
        for i, column in enumerate(columns):
            if column == "GroupChatIDs":
                users_dict[column] = result[i].split(",")
            else:
                if (column != "PromptTokensTotal") and (
                    column != "CompletionTokensTotal"
                ):
                    users_dict[column] = bool(result[i])
                else:
                    users_dict[column] = result[i]

        return users_dict

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

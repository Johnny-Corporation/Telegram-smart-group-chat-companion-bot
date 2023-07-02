
class Johnny:
    """Chat handler, assumes to be created as separate instance for each chat"""

    def __init__(
        self,
        id_: int,
        trigger_messages_count: int = 5,
        temporary_memory_size: int = 30,
        allow_dynamically_change_message_trigger_count: bool = True,
    ) -> None:
        """
        Args:
            id_ (int): chat id
            trigger_messages_count (int): sets the numbers of messages needed to trigger the bot in cycle.
            (eg: if set to 5, bot will read conversation each time after 5 new messages, only when there were no replies to bot's message)
            temporary_memory_size (int): sets number of messages given to GPT (eg: if set to 5, gpt will read only 5 last messages;
            This does not affect persistent memory! Persistent memory keeps whole conversation.)

        """
        self.id = id_
        self.trigger_messages_count = trigger_messages_count
        self.temporary_memory_size = temporary_memory_size
        self.allow_dynamically_change_message_trigger_count = (
            allow_dynamically_change_message_trigger_count
        )
        self.tokens_spent = 0

    def think(self):
        """reads last"""

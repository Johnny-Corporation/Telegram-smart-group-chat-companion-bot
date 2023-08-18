from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
import soundfile as sf
from utils.db_controller import Controller
import utils.gpt_interface as gpt
from utils.time_tracking import *
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import random
import json
from os import environ

from utils.functions import describe_image, get_file_content

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from __main__ import *
from utils.functions import (
    load_templates,
    generate_voice_message,
    to_text,
    video_note_to_audio,
    take_info_about_sub,
)

templates = load_templates("templates\\")

load_dotenv(".env")


db_controller = Controller()

functions_waiting_messages = {
    "google": "googling_question.txt",
    "read_from_link": "reading_from_link.txt",
    "generate_image": "generating_image.txt",
}


@dataclass
class Johnny:
    """Group handler, assumes to be created as separate instance for each chat"""

    bot: TeleBot
    chat_id: int
    bot_username: str
    temporary_memory_size: int = 20
    language_code: str = "eng"
    trigger_probability: float = 0.8
    model = "gpt-3.5-turbo"
    temperature: float = 1
    frequency_penalty: float = 0.2
    presence_penalty: float = 0.2
    answer_length: str = "as you need"
    sphere: str = ""
    system_content: str = ""
    allow_functions: bool = True

    def __post_init__(self):
        # list of lists, where each list follows format: [senders_name, text]

        self.activated = False

        self.lang_code = None

        self.messages_history = []
        self.messages_count = 0  # incremented by one each message, think() function is called when hit trigger_messages_count

        self.enabled = False
        self.dynamic_gen = False
        # Needed to store requested links and restrict repeating useless requests
        self.dynamic_gen_chunks_frequency = 30  # when dynamic generation is enabled, this value controls how often to edit telegram message, for example when set to 3, message will be updated each 3 chunks from OpenAI API stream
        self.voice_out_enabled = False
        self.total_spent_messages = 0  # prompt and completion messages
        self.last_function_request = None
        self.button_commands = []
        self.messages_to_be_deleted = []
        # Permissions
        self.subscription = "Free"
        self.permissions = {
            "Free": {  # {type_of_sub: {point: value_of_point}}
                "allowed_groups": 1,
                "messages_limit": 30,
                "temporary_memory_size_limit": 20,
                "dynamic_gen_permission": False,
                "sphere_permission": False,
                "temperature_permission": False,
                "frequency_penalty_permission": False,
                "presense_penalty_permission": False,
                "voice_output_permission": False,
                "generate_picture_permission": False,
            }
        }

        # User
        self.id_groups = []
        self.commercial_trigger = 0

        # Group
        self.owner_id = None

    def get_completion(self, allow_function_call=None):
        """Returns completion object and takes one time arguments."""
        return gpt.create_chat_completion(
            self.messages_history,
            reply=bool(self.message.reply_to_message),
            answer_length=self.answer_length,
            model=self.model,
            temperature=self.temperature,
            stream=self.dynamic_gen,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            use_functions=(
                self.allow_functions
                if allow_function_call is None
                else allow_function_call
            ),
        )

    def one_answer(self, message: Message, groups: dict):
        response = gpt.create_chat_completion(
            [[message.from_user.first_name, message.text]],
            lang=self.lang_code,
            reply=None,
            model=self.model,
        )
        messages_used = 1
        self.total_spent_messages += messages_used

        if message.chat.id < 0:
            groups[self.owner_id].total_spent_messages = self.total_spent_messages
        return gpt.extract_text(response)

    def new_message(self, message: Message, groups: dict) -> str:
        # --- Check on limit on groups of one men ---
        # if (
        #     len(groups[self.owner_id].id_groups)
        #     > groups[self.owner_id].permissions[self.subscription]["allowed_groups"]
        # ):
        #     self.bot.send_message(
        #         message.chat.id,
        #         templates[self.lang_code]["exceed_limit_on_groups.txt"],
        #     )

        #     groups[self.owner_id].id_groups.remove(message.chat.id)

        #     self.bot.leave_chat(message.chat.id)
        #     return

        # --- Converts other types files to text ---
        match message.content_type:
            case "document":
                text = "[FILE] Content:" + get_file_content(self.bot, message)
            case "photo":
                image_info = self.bot.get_file(message.photo[-1].file_id)
                image_url = f"https://api.telegram.org/file/bot{environ['BOT_API_TOKEN']}/{image_info.file_path}"
                text = "[IMAGE] Description:" + describe_image(image_url)
            case "text":
                text = message.text
            case "voice":
                text = to_text(self.bot, message)
            case "video_note":
                text = video_note_to_audio(self.bot, message)
            case _:
                return  # unsupported event type

        # --- Add message to database ---
        db_controller.add_message_event(
            self.chat_id,
            text,
            datetime.now(),
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            self.total_spent_messages,
        )
        self.message = message
        # --- Add message to temporary memory ---
        self.messages_history.append([message.from_user.first_name, text])
        if len(self.messages_history) == self.temporary_memory_size:
            self.messages_history.pop(0)

        # --- checks on enabling of Bot ---
        if not self.enabled:
            return

        # --- If user reach some value to messages, suggest buy a subscription ----
        if (
            self.commercial_trigger < 1
            and self.total_spent_messages > 10000
            and self.subscription == "Free"
        ):
            self.bot.send_message(
                message.chat.id,
                templates[self.lang_code]["suggest_to_buy.txt"],
                parse_mode="HTML",
            )
            self.commercial_trigger += 1

        # --- Checks on messages ---
        if (
            self.total_spent_messages
            >= self.permissions[self.subscription]["messages_limit"]
        ):
            self.bot.send_message(
                message.chat.id,
                templates[self.lang_code]["exceed_limit_on_messages.txt"],
            )
            self.total_spent_messages = self.permissions[self.subscription][
                "messages_limit"
            ]
            return
        elif (
            groups[self.owner_id].total_spent_messages
            >= self.permissions[self.subscription]["messages_limit"]
        ):
            self.bot.send_message(
                message.chat.id,
                templates[self.lang_code]["exceed_limit_on_messages.txt"],
            )
            groups[self.owner_id].total_spent_messages = self.permissions[
                self.subscription
            ]["messages_limit"]
            return

        if (
            ("@" + self.bot_username in text)
            or (
                message.reply_to_message
                and message.reply_to_message.from_user.username == self.bot_username
            )
            or (random() < self.trigger_probability)
        ):
            print(f"HISTORY OF MESSAGES IN JOHNNY:    {self.messages_history}")

            # --- GPT answer generation ---

            self.response = self.get_completion()

            text_answer = (
                self.dynamic_generation(self.response)
                if self.dynamic_gen
                else self.static_generation(self.response)
            )

            groups[self.owner_id].total_spent_messages = self.total_spent_messages

            # Adding GPT answer to db and messages_history
            db_controller.add_message_event(
                self.chat_id,
                str(text_answer),
                datetime.now(),
                "$BOT$",
                "$BOT$",
                self.bot_username,
                self.total_spent_messages,
            )

            self.messages_history.append(["$BOT$", text_answer])

    def static_generation(self, completion):
        """Takes completion object and returns text answer. Handles message in telegram"""

        # Check function call
        response_message = completion["choices"][0]["message"]

        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            argument = next(iter(function_args.values()))

            self.messages_to_be_deleted.append(
                self.bot.send_message(
                    self.message.chat.id,
                    templates[self.lang_code][functions_waiting_messages[function_name]].format(argument),
                    parse_mode="html",
                    disable_web_page_preview=True,
                )
            )

            # If this response is same as previous, do not allow function call in next request and notify user
            if self.last_function_request == (function_name, function_args):
                self.messages_to_be_deleted.append(
                    self.bot.send_message(
                        self.message.chat.id,
                        templates[self.lang_code]["Function call failed"].format(function_name),
                        parse_mode="html"
                    )
                )
                self.last_function_request = None
                return self.static_generation(
                    self.get_completion(allow_function_call=False)
                )

            self.last_function_request = (function_name, function_args)

            # Additional arguments
            additional_args = {}
            if function_name == "generate_image":
                additional_args = {"bot": self.bot, "chat_id": self.chat_id}

            # Saving function result to history
            self.messages_history.append(
                [
                    "$FUNCTION$",
                    gpt.get_official_function_response(
                        function_name,
                        function_args=function_args,
                        additional_args=additional_args,
                    ),
                ]
            )
            if function_name == "generate_image":
                return "[IMAGES]"  # this will be saved as bot message in history

            return self.static_generation(self.get_completion())

        self.delete_pending_messages()
        self.response = completion
        text_answer = gpt.extract_text(self.response)
        # Check context understanding
        if not self.check_understanding(text_answer):
            return None

        self.bot.send_message(self.message.chat.id, text_answer, parse_mode="Markdown")
        return text_answer

    def dynamic_generation(self, completion):
        """Takes completion object and returns text answer. Handles message in telegram"""

        if self.last_function_request is None:
            self.thinking_message = self.bot.send_message(
                self.chat_id, "🤔", parse_mode="Markdown"
            )

        text_answer = ""  # stores whole answer

        update_count = 1
        func_call = {
            "name": None,
            "arguments": "",
        }

        for res in completion:
            delta = res.choices[0].delta
            if "function_call" in delta:
                if "name" in delta.function_call:
                    func_call["name"] = delta.function_call["name"]
                if "arguments" in delta.function_call:
                    func_call["arguments"] += delta.function_call["arguments"]
            if res.choices[0].finish_reason == "function_call":
                # Handling function call

                function_name = func_call["name"]
                function_args = json.loads(func_call["arguments"])
                argument = next(iter(function_args.values()))

                self.messages_to_be_deleted.append(
                    self.bot.send_message(
                        self.message.chat.id,
                        functions_waiting_messages[function_name].format(argument),
                        disable_web_page_preview=True,
                    )
                )

                # If previous function call was the same as current
                if self.last_function_request == (function_name, function_args):
                    self.messages_to_be_deleted.append(
                        self.bot.send_message(
                            self.message.chat.id,
                            "(Function call failed)",
                        )
                    )
                    return self.dynamic_generation(
                        self.get_completion(allow_function_call=False)
                    )

                self.last_function_request = (function_name, function_args)

                # Additional arguments
                additional_args = {}
                if function_name == "generate_image":
                    additional_args = {"bot": self.bot, "chat_id": self.chat_id}

                self.messages_history.append(
                    [
                        "$FUNCTION$",
                        gpt.get_official_function_response(
                            function_name,
                            function_args=function_args,
                            additional_args=additional_args,
                        ),
                    ]
                )

                if function_name == "generate_image":
                    return "[IMAGES]"  # this will be saved as bot message in history

                return self.dynamic_generation(self.get_completion())
                # End of handling function call

            if ("content" in res["choices"][0]["delta"]) and (
                text_chunk := res["choices"][0]["delta"]["content"]
            ):
                text_answer += text_chunk
                update_count += 1

                if update_count == self.dynamic_gen_chunks_frequency:
                    update_count = 0
                    self.bot.edit_message_text(
                        chat_id=self.message.chat.id,
                        message_id=self.thinking_message.message_id,
                        text=text_answer,
                    )

        if update_count != 0:
            self.bot.edit_message_text(
                chat_id=self.message.chat.id,
                message_id=self.thinking_message.message_id,
                text=text_answer,
            )
        self.delete_pending_messages()
        return text_answer

    def check_understanding(self, text_answer: str) -> bool:
        """Checks if GPT understands context of the question"""

        # Checking context understating
        if (
            (self.trigger_probability != 1)
            and (self.trigger_probability != 0)
            and (not gpt.check_context_understanding(text_answer))
        ):
            return False

        # Checking model answer is about selected sphere
        if (
            (self.trigger_probability != 1)
            and (self.trigger_probability != 0)
            and (self.sphere)
            and (not gpt.check_theme_context(text_answer, self.sphere))
        ):
            return False
        # Count tokens !!!!
        return True

    def add_new_user(
        self,
        chat_id,
        first_name,
        last_name,
        username,
        type_of_subscription: str,
        messages_total: int,
    ):
        # get current date
        current_date = datetime.now().isoformat()

        # If the user already written in db, delete old vers
        if db_controller.check_the_existing_of_user_with_sub(int(chat_id)):
            db_controller.delete_the_existing_of_user_with_sub(int(chat_id))

        # Add to db
        db_controller.add_user_with_sub(
            chat_id,
            type_of_subscription,
            current_date,
            first_name,
            str(last_name),
            username,
            messages_total,
        )

        # If we wrote new user with new sub, give him 'congrats message'
        if type_of_subscription != "Free":
            self.bot.send_message(
                chat_id,
                templates[self.lang_code]["new_subscriber.txt"].format(
                    sub=type_of_subscription
                ),
                parse_mode="HTML",
            )

    def extend_sub(self, chat_id, first_name, last_name, username):
        # Get start date of current sub and add a month for extendtion
        date_of_start_txt = db_controller.get_last_date_of_start_of_user(chat_id)
        prev_date_of_start = datetime.fromisoformat(date_of_start_txt) + relativedelta(
            months=1
        )
        date_of_start = prev_date_of_start.isoformat()

        # Add copy of user but with extended date of user (The deleting of user with sub realized in sub_tracking)
        db_controller.add_user_with_sub(
            chat_id,
            self.subscription,
            self.allowed_groups,
            self.temporary_memory_size_limit,
            date_of_start,
            first_name,
            str(last_name),
            username,
            self.permissions[self.subscription]["messages_limit"],
        )

        self.bot.send_message(
            chat_id,
            templates[self.lang_code]["sub_extend.txt"].format(sub=self.subscription),
            parse_mode="HTML",
        )

    def delete_pending_messages(self):
        for m in self.messages_to_be_deleted:
            try:
                self.bot.delete_message(self.chat_id, m.message_id)
            except:
                pass
        self.messages_to_be_deleted.clear()

    def track_sub(self, chat_id: int, new: bool):
        def sub_tracking(chat_id: int, date_of_start):
            """This fucntion calls when subscription was ended (after month)"""

            # Add reminders!!!

            # Add current user from db with subscription
            db_controller.delete_the_existing_of_user_with_sub_by_date(date_of_start)

            # check the extendtion of
            check = db_controller.check_the_existing_of_user_with_sub(chat_id)

            # if there aren't more subscriptions, put free sub
            if not check:
                self.bot.send_message(
                    chat_id,
                    templates[self.lang_code]["sub_was_end.txt"],
                    parse_mode="HTML",
                )

                current_date = datetime.now().isoformat()

                db_controller.add_user_with_sub(
                    chat_id, "Free", current_date, " ", " ", " ", 50
                )

                self.subscription = "Free"

                self.permissions = {}

                permissions = take_info_about_sub(self.subscription)
                self.permissions[self.subscription] = permissions

                self.temperature = 1
                self.frequency_penalty = 0.2
                self.presense_penalty = 0.2
                self.sphere = ""
                self.temporary_memory_size = 20
                self.voice_out_enabled = False
                self.dynamic_gen = False

                return

            self.bot.send_message(
                chat_id,
                templates[self.lang_code]["sub_was_end_with_extend.txt"].format(
                    sub=self.subscription
                ),
                parse_mode="HTML",
            )

        if self.subscription == "SMALL BUSINESS (trial)":
            start_date_txt = db_controller.get_last_date_of_start_of_user(chat_id)
            start_date = datetime.fromisoformat(start_date_txt)

            # create a scheduler
            sub_scheduler = BackgroundScheduler()

            # schedule a task to print a number after 2 seconds
            sub_scheduler.add_job(
                sub_tracking,
                "date",
                run_date=start_date + relativedelta(days=3),
                args=[chat_id, start_date_txt],
                misfire_grace_time=86400,
            )

            # start the scheduler
            sub_scheduler.start()

        elif self.subscription != "Free":
            if new:
                start_date_txt = db_controller.get_last_date_of_start_of_user(chat_id)
                start_date = datetime.fromisoformat(start_date_txt)

                # create a scheduler
                sub_scheduler = BackgroundScheduler()

                # schedule a task to print a number after 2 seconds
                sub_scheduler.add_job(
                    sub_tracking,
                    "date",
                    run_date=start_date + relativedelta(months=1),
                    args=[chat_id, start_date_txt],
                    misfire_grace_time=86400,
                )

                # start the scheduler
                sub_scheduler.start()
            else:
                all_dates = db_controller.get_users_with_sub_by_chat_id(chat_id)

                for date in all_dates:
                    start_date_txt = date[0]
                    start_date = datetime.fromisoformat(start_date_txt)

                    # create a scheduler
                    sub_scheduler = BackgroundScheduler()

                    # schedule a task to print a number after 2 seconds
                    sub_scheduler.add_job(
                        sub_tracking,
                        "date",
                        run_date=start_date + relativedelta(months=1),
                        args=[chat_id, start_date_txt],
                        misfire_grace_time=86400,
                    )

                    # start the scheduler
                    sub_scheduler.start()

    def change_owner_of_group(self, username):
        new_user = db_controller.get_user_with_sub_by_username(username)
        return new_user

    def add_purchase_of_messages(self, chat_id, num_of_new_messages):
        new_total_messages = self.messages_limit + num_of_new_messages
        db_controller.update_messages_of_user_with_sub(chat_id, new_total_messages)

    def change_memory_size(self, size):
        self.temporary_memory_size = size
        self.messages_history = []
        self.load_data()

    def load_subscription(self, chat_id):
        data = db_controller.get_user_with_sub_by_chat_id(chat_id)

        if data != {}:
            self.subscription = data["TypeOfSubscription"]

            self.permissions = {}

            permissions = take_info_about_sub(self.subscription)
            self.permissions[self.subscription] = permissions

            self.permissions[self.subscription]["messages_limit"] = data[
                "MessagesTotal"
            ]

            self.owner_id = chat_id
            return True
        return False

    def load_data(self) -> None:
        """Loads data from to object from db"""
        recent_events = db_controller.get_last_n_message_events_from_chat(
            self.chat_id, self.temporary_memory_size
        )
        if not recent_events:
            return
        self.messages_history = db_controller.get_last_n_messages_from_chat(
            self.chat_id, self.temporary_memory_size
        )[::-1]
        for i in recent_events:
            if i[5] == "JOHNNYBOT":
                self.total_spent_messages = i
                break

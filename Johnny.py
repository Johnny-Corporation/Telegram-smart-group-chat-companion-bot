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
from utils.functions import num_messages_from_string, num_messages_from_messages
from os import remove, makedirs

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from __main__ import *
from utils.functions import load_templates, generate_voice_message, to_text, video_note_to_audio, take_info_about_sub

templates = load_templates("templates\\")


load_dotenv(".env")


db_controller = Controller()


@dataclass
class Johnny:
    """Group handler, assumes to be created as separate instance for each chat"""

    bot: TeleBot
    templates
    chat_id: int
    bot_username: str
    temporary_memory_size: int = 20     
    language_code: str = "eng"
    trigger_probability: float = 0.8
    model = "gpt-3.5-turbo"
    temperature: float = 1
    frequency_penalty: float = 0.2
    presense_penalty: float = 0.2
    answer_length: str = "as you need"
    sphere: str = ""
    system_content: str = ""
    """
    Args:
        id_ (int): chat id
        trigger_messages_count (int): sets the numbers of messages needed to trigger the bot in cycle.
        (eg: if set to 5, bot will read conversation each time after 5 new messages, only when there were no replies to bot's message)
        temporary_memory_size (int): sets number of messages given to GPT (eg: if set to 5, gpt will read only 5 last messages;
        This does not affect persistent memory! Persistent memory keeps whole conversation.)
        language_code (str): Language
        random_trigger (bool) If set to True, bot triggers randomly. When enabled, trigger_messages_count is ignored
        random_trigger_probability (float from 0 to 1) = Triggering probability on each message. Works only when random trigger is True 
        temperature (float) temperature value, used in requests to GPT
        
    """

    def __post_init__(self):
        # list of lists, where each list follows format: [senders_name, text]

        self.activated = False

        self.lang_code = None

        self.messages_history = []
        self.messages_count = 0  # incremented by one each message, think() function is called when hit trigger_messages_count

        self.enabled = False
        self.dynamic_gen = False
        self.dynamic_gen_chunks_frequency = 30  # when dynamic generation is enabled, this value controls how often to edit telegram message, for example when set to 3, message will be updated each 3 chunks from OpenAI API stream
        self.voice_out_enabled = False

        self.total_spent_messages = 0  # prompt and completion messages
        
        self.button_commands = []

        #Permissions
        self.subscription = "Free"
        self.permissions = {"Free":                               #{type_of_sub: {point: value_of_point}}
                              {
                                "allowed_groups": 1,
                                "messages_limit": 100,
                                "temporary_memory_size_limit": 20, 
                                "dynamic_gen_permission": False,
                                "sphere_permission": False,
                                "temperature_permission": False,
                                "frequency_penalty_permission": False,
                                "presense_penalty_permission": False,
                                "voice_output_permission": False,
                                "generate_picture_permission": False
                               }
                            }

        #User
        self.id_groups = []
        self.commercial_trigger = 0

        #Group
        self.owner_id = None


    def one_answer(self, message: Message, groups: dict):
        response = gpt.create_chat_completion(
            [[message.from_user.first_name, message.text]], lang=self.lang_code, reply=None, model=self.model
        )
        messages_used = gpt.extract_messages(response)
        self.total_spent_messages += messages_used

        if message.chat.id<0:
            groups[self.owner_id].total_spent_messages = self.total_spent_messages
        return gpt.extract_text(response)

    def new_message(
        self,
        message: Message,
        groups: dict
    ) -> str:

        # --- Check on limit on groups of one men ---
        if len(groups[self.owner_id].id_groups) > groups[self.owner_id].permissions[self.subscription]["allowed_groups"]:
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["exceed_limit_on_groups.txt"])

            groups[self.owner_id].id_groups.remove(message.chat.id)

            self.bot.leave_chat(message.chat.id)
            return

        
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
            self.total_spent_messages
        )
        # --- Add message to temporary memory ---
        self.messages_history.append([message.from_user.first_name, text])
        if len(self.messages_history) == self.temporary_memory_size:
            self.messages_history.pop(0)


        # --- checks on enabling of Bot ---
        if not self.enabled:
            return
        

        # --- If user reach some value to messages, suggest buy a subscription ----
        if self.commercial_trigger < 1 and self.total_spent_messages > 10000 and self.subscription == "Free":
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["suggest_to_buy.txt"], parse_mode='HTML')
            self.commercial_trigger += 1 


        # --- Checks on messages ---
        if self.total_spent_messages>=self.permissions[self.subscription]["messages_limit"]:
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["exceed_limit_on_messages.txt"])
            self.total_spent_messages = self.permissions[self.subscription]["messages_limit"]
            return
        elif groups[self.owner_id].total_spent_messages >=self.permissions[self.subscription]["messages_limit"]:
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["exceed_limit_on_messages.txt"])
            groups[self.owner_id].total_spent_messages = self.permissions[self.subscription]["messages_limit"]
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

            response = gpt.create_chat_completion(
                self.messages_history,
                lang=self.lang_code,
                reply=bool(message.reply_to_message),
                answer_length=self.answer_length,
                model=self.model,
                temperature=self.temperature,
                stream=self.dynamic_gen,
                frequency_penalty=self.frequency_penalty,
                presense_penalty=self.presense_penalty,
            )

            if self.dynamic_gen and self.dynamic_gen_permission:
                text_answer = ""  # stores whole answer
                bot_message = self.bot.send_message(
                    message.chat.id, "Thinking...", parse_mode="Markdown"
                )

                update_count = 1
                for i in response:
                    if ("content" in i["choices"][0]["delta"]) and (
                        text_chunk := i["choices"][0]["delta"]["content"]
                    ):
                        text_answer += text_chunk
                        update_count += 1

                        if update_count == self.dynamic_gen_chunks_frequency:
                            update_count = 0
                            self.bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=bot_message.message_id,
                                text=text_answer,
                            )

                self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=bot_message.message_id,
                    text=text_answer,
                )

            else:

                text_answer = gpt.extract_text(response)

                # Checking context understating
                if (
                    (self.trigger_probability != 1)
                    and (self.trigger_probability != 0)
                    and (not gpt.check_context_understanding(text_answer))
                ):
                    return
                # Checking model answer is about selected sphere
                if (
                    (self.trigger_probability != 1)
                    and (self.trigger_probability != 0)
                    and (self.sphere)
                    and (not gpt.check_theme_context(text_answer, self.sphere))
                ):
                    return

                # If message was a reply to bot message, bot will reply to reply

                if self.voice_out_enabled:
                    with open(generate_voice_message(message,text_answer), 'rb') as audio:
                        self.bot.send_voice(chat_id=message.chat.id, voice=audio)
                        audio_path = audio
                    remove(audio_path.name)
                    return
                
                self.bot.send_message(
                    message.chat.id, text_answer, parse_mode="Markdown"
                )

            # counting messages
            self.total_spent_messages += 1


            if message.chat.id<0:
                groups[self.owner_id].total_spent_messages = self.total_spent_messages

            # Adding GPT answer to db and messages_history
            db_controller.add_message_event(
                self.chat_id,
                text_answer,
                datetime.now(),
                "JOHNNYBOT",
                "JOHNNYBOT",
                self.bot_username,
                self.total_spent_messages,
            )
            self.messages_history.append(["assistant", text_answer])


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


        #If the user already written in db, delete old vers
        if db_controller.check_the_existing_of_user_with_sub(int(chat_id)):
            db_controller.delete_the_existing_of_user_with_sub(int(chat_id))

        #Add to db
        db_controller.add_user_with_sub(
            chat_id, 
            type_of_subscription,
            current_date,
            first_name,
            str(last_name),
            username,
            messages_total
        )

        #If we wrote new user with new sub, give him 'congrats message'
        if type_of_subscription != 'Free':
            self.bot.send_message(chat_id, self.templates[self.lang_code]["new_subscriber.txt"].format(sub=type_of_subscription), parse_mode="HTML")

        
    def extend_sub(self, chat_id, first_name, last_name, username):

        #Get start date of current sub and add a month for extendtion
        date_of_start_txt = db_controller.get_last_date_of_start_of_user(chat_id)
        prev_date_of_start = datetime.fromisoformat(date_of_start_txt) + relativedelta(months=1)
        date_of_start = prev_date_of_start.isoformat()

        #Add copy of user but with extended date of user (The deleting of user with sub realized in sub_tracking)
        db_controller.add_user_with_sub(
            chat_id, 
            self.subscription,
            self.allowed_groups,
            self.temporary_memory_size_limit,
            date_of_start,
            first_name,
            str(last_name),
            username,
            self.permissions[self.subscription]["messages_limit"]
        )

        self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_extend.txt"].format(sub=self.subscription), parse_mode="HTML")
        

    def track_sub(self, chat_id: int, new: bool):
        
        def sub_tracking(chat_id: int, date_of_start):
            """This fucntion calls when subscription was ended (after month)"""

            #Add reminders!!!

            #Add current user from db with subscription
            db_controller.delete_the_existing_of_user_with_sub_by_date(date_of_start)


            #check the extendtion of 
            check = db_controller.check_the_existing_of_user_with_sub(chat_id)

            #if there aren't more subscriptions, put free sub
            if not check:

                self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_was_end.txt"], parse_mode="HTML")

                current_date = datetime.now().isoformat()

                db_controller.add_user_with_sub(
                    chat_id, 
                    "Free",
                    current_date,
                    " ",
                    " ",
                    " ",
                    100
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

            self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_was_end_with_extend.txt"].format(sub=self.subscription), parse_mode="HTML")

        if self.subscription == "SMALL BUSINESS (trial)":

            start_date_txt = db_controller.get_last_date_of_start_of_user(chat_id)
            start_date = datetime.fromisoformat(start_date_txt)

            # create a scheduler
            sub_scheduler = BackgroundScheduler()

            # schedule a task to print a number after 2 seconds
            sub_scheduler.add_job(sub_tracking, 'date', run_date=start_date + relativedelta(days=3), args=[chat_id, start_date_txt], misfire_grace_time=86400)

            # start the scheduler
            sub_scheduler.start()
        
        elif self.subscription != "Free":

            if new:
                start_date_txt = db_controller.get_last_date_of_start_of_user(chat_id)
                start_date = datetime.fromisoformat(start_date_txt)

                # create a scheduler
                sub_scheduler = BackgroundScheduler()

                # schedule a task to print a number after 2 seconds
                sub_scheduler.add_job(sub_tracking, 'date', run_date=start_date + relativedelta(months=1), args=[chat_id, start_date_txt], misfire_grace_time=86400)

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
                    sub_scheduler.add_job(sub_tracking, 'date', run_date=start_date + relativedelta(months=1), args=[chat_id, start_date_txt], misfire_grace_time=86400)

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

            self.permissions[self.subscription]["messages_limit"] = data["MessagesTotal"]

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


# TODO
# [x] log events
# [x] always reply when tagging or replying
# [x] language change
# [x] Add gpt
# [x] Count messages
# [x] Ask question to bot (via reply)
# [x] test adding to group
# [x] dynamic generation
# [x] write input output messages to db
# [x] refactoring
# [x] help command, all commands with descriptions <<---------Misha
# [x] Convert templates with parse_html<<---------- Misha
# [x] Make support for german and spanish
# [x] Make sticker support only for ru
# [x] Configure gpt for correct answers
# [x] manual mode <<--------------- Misha
# [x] Assistant; User in messages history (refactor temporary memory)
# [x] Dialog mode <<------ Misha
# [ ] translate all templates <<------ Misha
# [x] interface of changing all parameters + customization
# [x] account info command\
# [x] conservations in private messages
# [x] /start fix
# [x] functions set presense + frequency penalties

# ------------ for today (11 july 23) -------------
# [x] fix dynamic generation
# [x] assign name to messages
# [x] Make GPT answer no, when it doesnt understand context
# [x] Generate system_content (maybe add some system contents) <<--------- Misha
# [x] run on sfedu
# [x] add to our group

#  ----------- later -----------
# [x] Count messages for dynamic generation via tokenizer <<-----------Misha
# [x] add all params like penalty max_messages etc

# ------------ future features ---------
# [ ] Internet access parameter
# [ ] Audio messages support (maybe do one of element of customization)
# [ ] games with gpt (entertainment part)
# [ ] gpt answers to message by sticker or emoji
# [ ] activation keys for discount
# [x] conservations in private messages
# [ ] automatic calling functions
# [ ] automatic commands detection
# [ ] document read

# for today (11 july 23)
# [x] add commands for developers
# [x] db operations
# [x] Maybe add to TODO
# [x] get logs
# [x] separate logs

# --- for matvey in train ---
# [x] separate commands in files
# [x] fix clients info saving
# [ ] db for subs
# [x] commands for developers


# [x] tests
# [x] new private init file
# [x]

# [x]  fix dynamic generation
# [x] internet access
# [x] speech to text

# [ ] Fix templates, rephrase strange texts


# [ ] Run on server

# [ ] TypeError fix
# [ ] QIWI payment
# [ ] KickStarted
# [ ] BoomStarted


# [x] Command to change group's owner
# [ ] Detect the developers in initializations
# [ ] english templates to other languages

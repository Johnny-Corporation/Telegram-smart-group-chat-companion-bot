import openai
from os import environ
from utils.logger import logger  # needed for hidden logs, do not remove
import utils.functions as functions
import json
from utils.internet_access import *

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def extract_text(completion: openai.ChatCompletion) -> str:
    """Extracts text from OpenAI API response"""
    return completion.choices[0].message.content


def check_function_call(completion: openai.ChatCompletion) -> bool:
    return bool(completion["choices"][0]["message"].get("function_call"))


def extract_function_call_details(completion: openai.ChatCompletion) -> dict:
    return {
        "name": completion["choices"][0]["message"]["function_call"]["name"],
        "args": json.loads(
            completion["choices"][0]["message"]["function_call"]["arguments"]
        ),
    }


def get_messages_in_official_format(messages):
    """Converts messages kept in Johnny to official format"""
    previous_messages = []
    for m in messages:
        if m[0] == "$FUNCTION$":
            previous_messages.append(m[1])
            continue
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "$BOT$" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )
    return previous_messages


def generate_image(prompt, n, size):
    """Returns links to image"""
    response = openai.Image.create(prompt=prompt, n=n, size=size)
    links = []
    for i in response["data"]:
        links.append(i["url"])
    return links


def generate_image_and_send(bot, chat_id, prompt, n=1, size="1024x1024"):
    """Returns message which will be added to history, prompt and info about image"""
    urls = generate_image(prompt, n, size)
    for url in urls:
        functions.send_image_from_link(bot, url, chat_id)

    return f"Function has sent {n} AI-generated image(s). (prompt:'{prompt}')"


def create_chat_completion(
    messages: list,
    lang: str = "en",
    system_content: str = None,
    answer_length: int = "as you need",
    use_functions: bool = False,
    reply: bool = False,  # SYS
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
) -> openai.ChatCompletion:
    """Creates ChatCompletion
    messages(list): list of dicts, where key is users name and value is his message
    reply(bool): True means GPT will consider last message, False means not, None means system input field will be empty
    """

    # --- Building system content ---
    system_content = "You are a group chat participant. "
    if reply:
        system_content += "Focus on the last message. "

    system_content += "Ask questions if you need. "
    system_content += f"Your answer should be {answer_length}. "

    previous_messages = [
        {
            "role": "system",
            "content": functions.translate_text(lang, system_content),
        }
    ]

    # --- Building messages ---

    previous_messages.extend(get_messages_in_official_format(messages))

    # --- Creating ChatCompletion object ---

    chat_completion_arguments = {
        "model": model,
        "messages": previous_messages,
        "temperature": temperature,
        "top_p": top_p,
        "n": n,
        "stream": stream,
        "stop": stop,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
    }
    if use_functions:
        chat_completion_arguments["functions"] = load_functions_for_gpt()
        chat_completion_arguments["function_call"] = "auto"

    # Context length exceeded
    # n = 2
    # while 1:
    #     try:
    completion = openai.ChatCompletion.create(**chat_completion_arguments)
    # except openai.error.InvalidRequestError:
    #     logger.warning(
    #         f"OpenAI API request failed, InvalidRequestError. Retrying... \n"
    #     )
    #     chat_completion_arguments["messages"] = previous_messages[
    #         len(previous_messages) // n :
    #     ]
    # else:
    #     break
    # n += 1

    logger.info(f"API completion object: {completion}")

    return completion


available_functions = {
    "google": google,
    "read_from_link": read_from_link,
    "generate_image": generate_image_and_send,
}


def get_official_function_response(
    function_name: str, function_args: dict, additional_args: dict = {}
) -> list:
    """Takes function name and arguments and returns official response (dict in list)"""

    function_to_call = available_functions[function_name]
    args = {**function_args, **additional_args}
    function_response = function_to_call(**args)
    return {
        "role": "function",
        "name": function_name,
        "content": str(function_response),
    }


def load_functions_for_gpt():
    with open("utils\\gpt_functions_description.json") as f:
        return json.load(f)


def check_context_understanding(answer):
    """Returns bool - True if model answer assumes model understands context else False"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"This is text model's answer: {answer}. Is model saying it doesn't understand context and/or just trying to keep up conversation? Answer Yes or No",
            }
        ],
        temperature=0,
        max_messages=1,
    )
    return extract_text(completion) == "No"


def check_theme_context(answer, theme):
    """Returns bool - True is answer is related to theme, False if not"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"This is text model's answer: {answer}. Is model saying something about {theme}? Answer Yes or No",
            }
        ],
        temperature=0,
        max_messages=1,
    )
    return extract_text(completion) == "Yes"


def get_messages_in_official_format(messages):
    """Converts messages kept in Johnny to official format"""
    previous_messages = []
    for m in messages:
        if m[0] == "$FUNCTION$":
            previous_messages.append(m[1])
            continue
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "$BOT$" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )
    return previous_messages


def speech_to_text(path):
    audio_file = open(path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text

import openai
from os import environ
from utils.logger import logger  # needed for hidden logs, do not remove
import utils.functions as functions

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def extract_tokens(completion: openai.ChatCompletion) -> int:
    """Extracts tokens from OpenAI API response"""
    return [completion.usage.prompt_tokens, completion.usage.completion_tokens]


def extract_text(completion: openai.ChatCompletion) -> str:
    """Extracts text from OpenAI API response"""
    return completion.choices[0].message.content


def create_chat_completion(
    messages: list,
    system_content: str = "You are helpful assistant",
    answer_length: int = None,
    sphere: str = "",
    reply: bool = False,  # SYS
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presense_penalty: float = 0,
) -> openai.ChatCompletion:
    """Creates ChatCompletion
    messages(list): list of dicts, where key is users name and value is his message
    reply(bool): True means GPT will consider last message, False means not, None means system input field will be empty
    """

    # Build the system_content
    system_content = "If you don't understand context, say 'NO' and i will handle it. "

    if reply:
        system_content += "Focus on the last message. "

    system_content += "Keep up the conversation, ask questions if you need. "
    system_content += f"Your answer should be {answer_length}. "
    if sphere != "":
        system_content += "The conservation is about " + sphere + ". "

        # Got memory
    previous_messages = [
        {
            "role": "system",
            "content": system_content,
        }
    ]

    for m in messages:
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "assistant" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )

    completion = openai.ChatCompletion.create(
        model=model,
        messages=previous_messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presense_penalty,
    )

    return completion

import openai
from os import environ
from logger import logger

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def extract_tokens(completion):
    """Extracts tokens from OpenAI API response"""
    return [completion.usage.prompt_tokens, completion.usage.completion_tokens]


def extract_text(completion):
    """Extracts text from OpenAI API response"""
    return completion.choices[0].message.content


def create_chat_completion(
    messages: list,
    reply: bool = False,
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
) -> openai.Completion:
    """Creates ChatCompletion
    messages(list): list of strings
    reply(bool): True means GPT will consider last message, False means not, None means system input field will be empty
    """
    if reply != None:
        system_content = "Ifr u are not sure u understand context, say 'NO' and i will handle it. Be brief, answer in 1-2 short sentences. Keep up the conversation, ask questions if u want. Message example: 'Matvey:Hey', this means user with name 'Matvey' said 'Hey'. Dont include your name or role in response. '@' sign means tagging and people are waiting reaction"
        if reply:
            system_content += " Write the answer or suggestions to the last message"
    else:
        system_content = "be a polite helper"

    previous_messages = [{"role": "system", "content": system_content}]
    for i in messages:
        previous_messages.append({"role": "user", "content": i})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=previous_messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return completion


def dialog_mode(    
    messages: list,
    last_message: str,
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
) -> openai.Completion:
    
    system_content = "You are helpful assistant"

    previous_messages = [
        {"role": "system", "content": system_content}
        ]

    # --- add previous messages to gpt ---
    for i in messages:
        previous_messages.append({"role": "user", "content": i[0]})
        previous_messages.append({"role": "assistant", "content": i[1]})

    # --- add last user message to gpt ---
    previous_messages.append({"role": "user", "content": last_message})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=previous_messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return completion


def manual_mode(
    messages: list,
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
) -> openai.Completion:
    
    system_content = "You are helpful assistant"

    previous_messages = [
        {"role": "system", "content": system_content}
        ]

    # --- add previous messages to gpt ---
    for i in messages:
        if 'U: ' in i[0:3]:
            previous_messages.append({"role": "user", "content": i[3:]})
        elif 'B: 'in i[0:3]:
            previous_messages.append({"role": "assistant", "content": i[3:]})
        else:
            previous_messages.append({"role": "user", "content": i})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=previous_messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return completion
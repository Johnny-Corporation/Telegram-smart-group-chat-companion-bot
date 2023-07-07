import openai
from os import environ
from logger import logger

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def check_negative_answer(text: str) -> bool:
    """Checks wether input text is negative answer or not"""
    pass


def chat_message(context: list) -> str:
    pass


def one_question(
    text: str,
    model="gpt-3.5-turbo",
    temperature=0,
    top_p=0.1,
    n=1,
    stream=False,
    stop="\n",
    frequency_penalty=0,
    presence_penalty=0,
) -> dict:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Be brief"},
            {"role": "user", "content": text},
        ],
        # max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    logger.info(
        f"[Question to bot - request to GPT] Input: {text}; Output: {response.choices[0].message.content} Total tokens used: {response.usage.total_tokens}"
    )
    return response


def get_tokens(completion):
    tokens_total = [completion.usage.prompt_tokens,completion.usage.completion_tokens]
    return tokens_total


def get_text(completion):
    return completion.choices[0].message.content


def gpt_answer(
    memory,
    reply: bool,
    model="gpt-3.5-turbo",
    temperature=0,
    top_p=0.1,
    n=1,
    stream=False,
    stop=None,
    frequency_penalty=0,
    presence_penalty=0,
):
    # --- check the replying and create ---
    if reply == True:
        system_content = "Write the answer or suggestions to the last message"
    else:
        system_content = "Read previous messages and write something useful"

    # --- transform previous messages to gpt_supported view ---
    previous_messages = [{"role": "system", "content": system_content}]

    # --- add messages to gpt ---
    for i in memory:
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

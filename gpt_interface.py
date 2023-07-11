import openai
from os import environ
from logger import logger
import functions

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
    system_content: str="You are helpful assistant",
    answer_length: str="",
    sphere: str="",
    reply: bool = False,            #SYS
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presense_penalty: float = 0
) -> openai.ChatCompletion:
    """Creates ChatCompletion
    messages(list): list of dicts, where key is users name and value is his message
    reply(bool): True means GPT will consider last message, False means not, None means system input field will be empty
    """


    #Got memory
    previous_messages = [{"role": "system", "content": "If u are don't understand understand context, say 'NO' and i will handle it. If you understand context say something else."}]

    for m in messages:
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "assistant" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )

    



    # System content

    #Check the context
    if reply != None:
        understand_context_completion = openai.ChatCompletion.create(
            model=model,
            messages=previous_messages,
            temperature=0,
            top_p=top_p,
            n=n,
            stream=False,
            stop=stop,
            frequency_penalty=0,
            presence_penalty=0,
        )
        if extract_text(understand_context_completion) == 'NO':
            return understand_context_completion
        

        #Build the system_content
        system_content = ""
        
        if reply:
            system_content = "Focus on the last message. "


    
        system_content = system_content + "Keep up the conversation, ask questions if u need. "
        system_content = system_content + "Your answer must be " + answer_length + '. '
        if sphere != "":
            system_content = system_content + "The conservation about " + sphere + '. '

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!            '  ,reply, '              !!!!!!!!!!!!!!!!!!!!!!')

    previous_messages[0] = {"role": "system", "content": system_content}


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

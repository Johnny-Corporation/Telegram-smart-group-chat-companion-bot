import os
import openai

def conservation(gpt_token, organization_token ,model, system_content, user_content, memory):
    
    openai.api_key = str(gpt_token)
    openai.organization = organization_token

    #transform previous messages to gpt_supported view
    previous_messages = [
        {"role": "system", "content": system_content},
        ]

    for i in range(1,len(memory)):
        previous_messages.append({"role": "user", "content": memory[i][0]})
        previous_messages.append({"role": "assistant", "content": memory[i][1]})

    #add last user message to gpt
    previous_messages.append({"role": "user", "content": user_content})


    completion = openai.ChatCompletion.create(
        model=model,
        messages=previous_messages
    )
    
    return completion
    
    


def question_to_bot(gpt_token,organization_token,message):

    message_to_gpt = ''

    try:
        message.index(' ')
    except:
        return 'You sent an empty message to gpt'


    for i in range(message.index(' ')+1, len(message)):
        message_to_gpt = message_to_gpt + message[i]

    model = "gpt-3.5-turbo" #!!!!!!!!!!!!!!!!!!!!!!!!!1Can be changed (connect with more global)!!!!!!!!!!!!!!!!!
    system_content = 'Answer the question' #!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!!!!!!!!!!!!!

    return get_response(message_to_ai(gpt_token,organization_token,model,system_content,message_to_gpt))

def message_to_ai(gpt_token, organization_token ,model, system_content, user_content):
    
    openai.api_key = str(gpt_token)
    openai.organization = organization_token


    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )

    return completion

def get_tokens(completion):
    tokens_total = completion.usage.total_tokens

    #print(f"Tokens: {tokens_total}")

    return tokens_total

def get_response(completion):

    #print(f"Message: {message_back}")

    return completion.choices[0].message.content


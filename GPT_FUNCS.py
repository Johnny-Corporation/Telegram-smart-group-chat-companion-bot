import os
import openai

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


import openai


openai.api_key = "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"

response = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": "Be brief"},
        {"role": "user", "content": text},
    ],
    max_tokens=max_tokens,
    temperature=temperature,
    top_p=top_p,
    n=n,
    stream=stream,
    stop=stop,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty,
)

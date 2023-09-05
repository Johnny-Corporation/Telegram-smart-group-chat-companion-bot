from utils.gpt_interface import generate_suggestion_for_inline
import asyncio
from aiohttp import ClientSession
import openai

async def get_gpt_results(query, num_results=2):
    results = []
    
    verbose = num_results == 1

    openai.aiosession.set(ClientSession())
    tasks = [generate_suggestion_for_inline(query,verbose) for _ in range(num_results)]
    suggestions = await asyncio.gather(*tasks)
    await openai.aiosession.get().close()
    
    for sug in suggestions:
        try:
            if not verbose:
                title, description, body = sug.split("|")
            else:
                title = "✅"
                description = sug
                body = sug
        except:
            continue
        results.append(
            {
                "has_button": False,
                "title": title,
                "message_text": body,
                "thumbnail": "https://mrvian.com/wp-content/uploads/2023/02/logo-open-ai.png",
                "description": description,
            }
        )
    if not results:
        results.append(
            {
                "has_button": False,
                "title": "Sorry, generation failed",
                "message_text": "Generation Failed",
                "thumbnail": "https://blog.hubspot.com/hs-fs/hubfs/http-error-500-google.webp?width=650&height=462&name=http-error-500-google.webp",
                "description": "500: Internal server error",
            }
        )
    return results

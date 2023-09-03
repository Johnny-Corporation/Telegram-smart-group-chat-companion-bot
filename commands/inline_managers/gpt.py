from utils.gpt_interface import get_gpt_inline_suggestions


def get_gpt_results(query, num_results=2):
    results = []
    
    verbose = num_results == 1

    for i in range(num_results):
        suggestion = get_gpt_inline_suggestions(query,verbose=verbose)
        try:
            if not verbose:
                title, description, body = suggestion.split("|")
            else:
                title = "✅"
                description = suggestion
                body = suggestion
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

import requests
from bs4 import BeautifulSoup


def get_google_results(query):
    results = []

    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.select(".kCrYT a")
    for i, result in enumerate(search_results):
        if not result.get_text():
            continue
        if result["href"].startswith("http"):
            results.append(
                {
                    "has_button": True,
                    "button_text": "↗",
                    "button_link": result["href"],
                    "title": result.get_text(),
                    "message_text": f">>> Google <<<\n{result.get_text()}",
                    "thumbnail": "https://assets.stickpng.com/images/5847f9cbcef1014c0b5e48c8.png",
                    "description": result["href"],
                }
            )
        else:
            results.append(
                {
                    "has_button": True,
                    "button_text": "↗",
                    "button_link": "https://www.google.com" + result["href"],
                    "title": result.get_text(),
                    "message_text": f"Google \n{result.get_text()}",
                    "thumbnail": "https://assets.stickpng.com/images/5847f9cbcef1014c0b5e48c8.png",
                    "description": "https://www.google.com" + result["href"],
                }
            )
    return results

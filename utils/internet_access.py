import requests
from bs4 import BeautifulSoup
from utils.logger import logger
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def google(question: str) -> str:
    logger.info(f'google function called, question: "{question}"')

    url = "https://www.google.com/search?q=" + question
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.select(".kCrYT a")
    result_string = ""
    for i, result in enumerate(search_results):
        if "accuweather" in result["href"]:
            continue
        if result["href"].startswith("http"):
            result_string += f"{result.get_text()} - {result['href']}\n"
        else:
            result_string += (
                f"{result.get_text()} - {'https://www.google.com'+result['href']}\n"
            )
        if i == 4:  # 5 top results
            break

    logger.debug(f"Results from google search: {result_string}")

    return result_string


def remove_scripts_and_styles(html):
    return re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)

def extract_text(input_string):
    result = ""
    for i in re.findall(r'>\s*(.*?)(?:<|$)', input_string):
        if i:
            result += i + "|"
    return result

def read_from_link(link: str) -> str:
    logger.info(f'read_from_link function called, requested link: "{link}"')

    try:
        response = requests.get(link, timeout=5, headers=headers)
    except requests.exceptions.RequestException:
        return "Sever is not responding, cant read link"
    all_visible_text = extract_text(remove_scripts_and_styles(response.content.decode()))
    all_text = all_visible_text[:5000]

    logger.info(f"Text parsed form link {link}:{all_text}")

    return all_text

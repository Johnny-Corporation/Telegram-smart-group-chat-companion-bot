from __main__ import *
import uuid
from utils.functions import translate_text

from commands.inline_managers.google import *
from commands.inline_managers.gpt import *
from commands.inline_managers.youtube import *


from telebot.apihelper import ApiTelegramException
import asyncio


@bot.inline_handler(lambda query: True)
def inline_search(query):
    chat_id = query.from_user.id
    search_query = query.query
    print("===============================", query, query.query)
    """
    Each function must return list of dicts, in every dicts next fields are awaited:
        has_button: bool, required
        button_text: str, optional
        button_link: str, optional
        title: str, required
        description: str, optional
        message_text: str, required
        thumbnail: str, optional
    """

    thumbnails = {
        "Google": "https://assets.stickpng.com/images/5847f9cbcef1014c0b5e48c8.png",
        "Youtube": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/YouTube_social_white_square_%282017%29.svg/1200px-YouTube_social_white_square_%282017%29.svg.png",
        "GPT": "https://mrvian.com/wp-content/uploads/2023/02/logo-open-ai.png",
    }

    dont_change_cache_time = False

    if (chat_id not in groups) or (groups[chat_id].lang_code is None):
        results = [
            {
                "has_button": False,
                "title": "Start",
                "message_text": f"Register in @JohnnyAIBot to use inline",
                "thumbnail": "https://replicate.delivery/pbxt/Lca3IEjcKoJBBVS6ajROkK37sDzPsmjYxIcFzxPZp65wZzTE/out-0.png",
                "description": "Run Johnny",
            }
        ]
        cache_time = 1  # if user registered but didnt set lang, we also will force him to register, this is important
        dont_change_cache_time = True
    elif search_query == "":  # Just triggered inline, haven't started typing
        results = [
            {
                "has_button": False,
                "title": groups[chat_id].inline_mode,
                "message_text": "...",
                "thumbnail": thumbnails[groups[chat_id].inline_mode],
                "description": translate_text(
                    groups[chat_id].lang_code, "Current mode. Just start typing."
                ),
            }
        ]
    else:
        match groups[chat_id].inline_mode:
            case "Google":
                results = get_google_results(search_query)
            case "GPT":
                results = asyncio.run(
                    get_gpt_results(
                        search_query,
                        num_results=groups[chat_id].num_inline_gpt_suggestions,
                    )
                )
            case "Youtube":
                results = get_youtube_results(search_query)

    # --- Building inline response ---
    articles = []
    for result in results:
        unique_id = str(uuid.uuid4())
        if result["has_button"]:
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                result["button_text"], url=result["button_link"]
            )
            keyboard.add(btn)
        kwargs = {
            "id": unique_id,
            "title": result["title"],
            "input_message_content": types.InputTextMessageContent(
                message_text=result["message_text"]
            ),
        }
        if result["has_button"]:
            kwargs["reply_markup"] = keyboard
        if result.get("thumbnail"):
            kwargs["thumbnail_url"] = result["thumbnail"]
        if result.get("description"):
            kwargs["description"] = result["description"]

        article = types.InlineQueryResultArticle(**kwargs)
        articles.append(article)

    try:
        if chat_id in groups:
            if not dont_change_cache_time:
                if groups[chat_id].inline_mode == "GPT":
                    cache_time = 86400  # maximum possible cache time (24hrs)
                elif groups[chat_id].inline_mode == "Google":
                    cache_time = 1  # 1 second
                elif groups[chat_id].inline_mode == "Youtube":
                    cache_time = 1  # 1 second
        else:
            cache_time = 1
        # cache_time = 1
        bot.answer_inline_query(query.id, articles, cache_time=cache_time)
    except ApiTelegramException as e:
        if e.error_code == 400:
            pass
        else:
            raise e


# Works only after enabling sending inline feedback via BotFather
# /setinlinefeedback
@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def extend_gpt_prompt(chosen_inline_result):
    # if chosen_inline_result.id not in inline_results_by_gpt:
    #     return

    print("========================================")
    print(chosen_inline_result)

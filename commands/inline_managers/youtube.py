from youtubesearchpython import VideosSearch


def get_youtube_results(query):
    results = []

    videos_search = VideosSearch(query, limit=10)

    for i in videos_search.result()["result"]:
        print(i)
        message_text = i["accessibility"]["title"] + "\n" + i["link"]
        results.append(
            {
                "has_button": True,
                "button_text": "YouTube",
                "button_link": i["link"],
                "title": i["title"],
                "message_text": message_text,
                "thumbnail": i["thumbnails"][0]["url"],
                "description": f"{i['publishedTime']} · {i['duration']} · {i['viewCount']['short']}",
            }
        )
    return results


# example
{
    "type": "video",
    "id": "rfscVS0vtbw",
    "title": "Learn Python - Full Course for Beginners [Tutorial]",
    "publishedTime": "5 years ago",
    "duration": "4:26:52",
    "viewCount": {"text": "41,509,353 views", "short": "41M views"},
    "thumbnails": [
        {
            "url": "https://i.ytimg.com/vi/rfscVS0vtbw/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD-9-7sK2ChwTaU2oDci15jO7wEDg",
            "width": 360,
            "height": 202,
        },
        {
            "url": "https://i.ytimg.com/vi/rfscVS0vtbw/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLABBQtpk83-Gm8-IgPAiGlTtrLH9w",
            "width": 720,
            "height": 404,
        },
    ],
    "richThumbnail": {
        "url": "https://i.ytimg.com/an_webp/rfscVS0vtbw/mqdefault_6s.webp?du=3000&sqp=CMTtz6cG&rs=AOn4CLAXOaA6aCzgLAg8oQAsyVUZGpEWpA",
        "width": 320,
        "height": 180,
    },
    "descriptionSnippet": [
        {
            "text": "This course will give you a full introduction into all of the core concepts in "
        },
        {"text": "python", "bold": True},
        {"text": ". Follow along with the videos and you'll be a\xa0..."},
    ],
    "channel": {
        "name": "freeCodeCamp.org",
        "id": "UC8butISFwT-Wl7EV0hUK0BQ",
        "thumbnails": [
            {
                "url": "https://yt3.ggpht.com/ytc/AOPolaTs1IEit9EUooQAJkWS4SkpUE7oMDXYrjIgnOk1Kw=s68-c-k-c0x00ffffff-no-rj",
                "width": 68,
                "height": 68,
            }
        ],
        "link": "https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ",
    },
    "accessibility": {
        "title": "Learn Python - Full Course for Beginners [Tutorial] by freeCodeCamp.org 5 years ago 4 hours, 26 minutes 41,509,353 views",
        "duration": "4 hours, 26 minutes, 52 seconds",
    },
    "link": "https://www.youtube.com/watch?v=rfscVS0vtbw",
    "shelfTitle": None,
}

from __main__ import *


# --- reply handler for img prompt ---
@error_handler
def img_prompt_reply_handler(inner_message):
    lang_code = groups[inner_message.chat.id].lang_code
    original_prompt = translate_text("en", inner_message.text, force=True)
    enhanced_prompt = improve_img_gen_prompt(original_prompt)
    sent_message = bot.send_message(
        inner_message.chat.id,
        translate_text(lang_code, "🎨🤖Generating image...")
        + (
            f" (Shown only for developers Prompt:{enhanced_prompt})"
            if (str(inner_message.chat.id) in developer_chat_IDs)
            else ""
        ),
    )
    bot.send_chat_action(inner_message.chat.id, "upload_photo")
    if groups[inner_message.chat.id].subscription != "Free":
        quality = "rich"
        bot.send_message(
            inner_message.chat.id, templates[lang_code]["long_image_generation.txt"]
        )
    else:
        quality = "poor"
    generate_image_and_send(bot, inner_message.chat.id, enhanced_prompt, size=quality)

    groups[inner_message].total_spent_messages += 1

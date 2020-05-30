#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import random
from datetime import datetime

import pytz
import telebot
from telebot import types, apihelper

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

# read config from config.json
with open("./config.json", "r+") as config_file:
    config = json.load(config_file)
    logger.info("Config file load successfully:\n" + str(config))
    bot_token = config["bot_token"]
    bot_https_proxy = config["bot_https_proxy"]
    timezone = config["timezone"]

# proxy setting
if bot_https_proxy != "":
    proxy = {'https': bot_https_proxy}
    apihelper.proxy = proxy

# bot token
bot = telebot.TeleBot(bot_token)

# custom nickname by detect userID
custom_nickname = {
    400521524: "小熊",
    407635222: "Lore酱 | ☆可爱 verified by LittleBear",
    223347749: "47",
    638996316: "47",
    602231778: "荔枝",
    459094099: "mashiro | 永远喜欢 菡",
    254030480: "KingCapri",
    73322551: "柯柯",
    137105537: "成本",
    557153656: "妹抖猫四",
    239887702: "Yooooooru",
}
random_stickers = ["CAADBQADvgYAAvjGxQoD_y6N-wJ3BwI",
                   "CAADBQADOAYAAvjGxQrGnfgTD5nfwQI"]
sleep_reminder = ["小可爱还没有睡觉吗？", "快去睡觉了啦！", "她已经睡着了喔…", "你的小可爱已经是守夜冠军了！"]


def get_time():
    # get local time
    cst_tz = pytz.timezone(timezone)
    now_time = datetime.now().replace(tzinfo=cst_tz)
    logger.debug("now time: " + now_time.strftime("%Y-%m-%d %H:%M:%S"))
    c_time = now_time.now().hour
    # change greeting text depend on time
    if 0 <= c_time < 4:
        greetings_type = "睡觉"
    elif 4 <= c_time < 11:
        greetings_type = "早安"
    elif 11 <= c_time < 14:
        greetings_type = "中午好"
    elif 14 <= c_time < 18:
        greetings_type = "下午好"
    elif 18 <= c_time < 22:
        greetings_type = "晚上好"
    elif 22 <= c_time < 24:
        greetings_type = "晚安"
    return greetings_type


def get_sender_name_and_id(message):
    if message.from_user.id in custom_nickname:
        send_name = custom_nickname[message.from_user.id]
    else:
        send_name = str(message.from_user.first_name)

    from_id = str(message.from_user.id)
    return send_name, from_id


def get_reply_name_and_id(message):
    # if nickname recorded
    if message.reply_to_message.from_user.id in custom_nickname:
        reply_name = custom_nickname[message.reply_to_message.from_user.id]
    else:
        reply_name = str(message.reply_to_message.from_user.first_name)
    reply_id = str(message.reply_to_message.from_user.id)
    return reply_name, reply_id


@bot.message_handler(content_types=["document", "audio", "photo", "sticker", "audio"])
def echo(message):
    logger.debug(message)


try:
    @bot.message_handler(commands=["greeting"])
    def greeting(message):
        greetings_type = get_time()
        send_name, from_id = get_sender_name_and_id(message)

        # if not reply to anyone
        if message.reply_to_message is None:
            if greetings_type == "睡觉":
                randNum = random.randint(0, 100)
                if randNum % 5 == 0:
                    bot.send_message(
                        message.chat.id,
                        "下面我宣布！[{send_name}](tg://user?id={from_id}) 是守夜冠军啦！".format(
                            send_name=send_name, from_id=from_id
                        ),
                        parse_mode="Markdown",
                    )
                    bot.send_document(
                        message.chat.id, "CgADBQADkAADdcmxV9tAyTZinfacAg")
                    greetings_type = "晚安"
                else:
                    greetings_type = "晚安"
            greetings_type = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～".format(
                send_name=send_name, from_id=from_id, txt=greetings_type
            )
            bot.send_message(message.chat.id, greetings_type, parse_mode="Markdown")
        else:
            # if it is a reply message
            if (
                    not message.from_user.id == message.reply_to_message.from_user.id
                    and not message.reply_to_message.from_user.username == "goodnight_prpr_bot"
            ):
                reply_name, reply_id = get_reply_name_and_id(message)
                if greetings_type == "早安":
                    randNum = random.randint(0, 100)
                    if randNum % 5 == 0:
                        bot.send_sticker(
                            message.chat.id, "CAADBQADGgUAAvjGxQrFBpd8WnW-TwI"
                        )
                        greetings_type = "[{reply_name}](tg://user?id={reply_id})～ [{send_name}](tg://user?id={from_id}) 爱你哦～".format(
                            reply_name=reply_name,
                            reply_id=reply_id,
                            send_name=send_name,
                            from_id=from_id,
                        )
                    else:
                        greetings_type = "[{send_name}](tg://user?id={from_id}) 向 [{reply_name}](tg://user?id={reply_id}) 道 {txt}～".format(
                            send_name=send_name,
                            from_id=from_id,
                            reply_name=reply_name,
                            reply_id=reply_id,
                            txt=greetings_type,
                        )
                        # send reply and delete command message
                        bot.reply_to(
                            message.reply_to_message, greetings_type, parse_mode="Markdown"
                        )
                elif greetings_type == "睡觉":
                    randNum = random.randint(0, 100)
                    if randNum % 5 == 0:
                        randReminder = random.randint(
                            0, len(sleep_reminder) - 1)
                        greetings_type = sleep_reminder[randReminder]
                    else:
                        greetings_type = "[{send_name}](tg://user?id={from_id}) 向 [{reply_name}](tg://user?id={reply_id}) 道 晚安～".format(
                            send_name=send_name,
                            from_id=from_id,
                            reply_name=reply_name,
                            reply_id=reply_id,
                        )
                    # send reply and delete command message
                    bot.reply_to(message.reply_to_message,
                                 greetings_type, parse_mode="Markdown")
                else:
                    randNum = random.randint(0, 100)
                    if randNum % 5 == 0:
                        randStick = random.randint(0, len(random_stickers) - 1)
                        bot.send_sticker(
                            message.chat.id, random_stickers[randStick])
                    greetings_type = "[{send_name}](tg://user?id={from_id}) 向 [{reply_name}](tg://user?id={reply_id}) 道 {txt}～".format(
                        send_name=send_name,
                        from_id=from_id,
                        reply_name=reply_name,
                        reply_id=reply_id,
                        txt=greetings_type,
                    )
                    # send reply and delete command message
                    bot.reply_to(message.reply_to_message,
                                 greetings_type, parse_mode="Markdown")
        # bot.delete_message(message.chat.id, message.message_id)


    # inline mode
    @bot.inline_handler(func=lambda query: True)
    def query_text(inline_query):
        try:
            logger.debug(inline_query)
            send_name, from_id = get_sender_name_and_id(inline_query)
            greetings_type = get_time()
            if greetings_type == "睡觉":
                greetings_type = "晚安"
            message_text = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～".format(
                send_name=send_name, from_id=from_id, txt=greetings_type
            )
            inline_greeting_results = types.InlineQueryResultArticle(
                "1", "向大家问好", types.InputTextMessageContent(
                    message_text, parse_mode="Markdown")
            )
            if len(inline_query.query) != 0:
                if inline_query.query[0] == "@":
                    inline_greeting_results_text = "{send_name} 向 {reply_name} 道 {txt}～".format(
                        send_name=send_name, reply_name=inline_query.query, txt=greetings_type
                    )
                    inline_greeting_results_with_someone = types.InlineQueryResultArticle(
                        "2",
                        "向{reply_name}问好".format(
                            reply_name=inline_query.query),
                        types.InputTextMessageContent(inline_greeting_results_text),
                    )
                    bot.answer_inline_query(
                        inline_query.id,
                        [inline_greeting_results, inline_greeting_results_with_someone],
                        cache_time=0,
                        is_personal=False,
                    )
            else:
                bot.answer_inline_query(
                    inline_query.id, [inline_greeting_results], cache_time=0, is_personal=False
                )
        except Exception as exception:
            logger.error(exception)


    bot.polling(none_stop=True)
# catch exception
except KeyboardInterrupt:
    quit()
except Exception as exception:
    logger.error(exception)

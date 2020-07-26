#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import random
import sqlite3
import time
from datetime import datetime, timedelta

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
    578175532: "蕾蕾",
}
random_stickers = ["CAADBQADvgYAAvjGxQoD_y6N-wJ3BwI",
                   "CAADBQADOAYAAvjGxQrGnfgTD5nfwQI"]
sleep_reminder = ["小可爱还没有睡觉吗？", "快去睡觉了啦！", "她已经睡着了喔…", "你的小可爱已经是守夜冠军了！"]


def get_time():
    # get local time
    cst_tz = pytz.timezone(timezone)
    now_time = datetime.now().replace(tzinfo=cst_tz)
    return now_time


def get_time_type():
    now_time = get_time()
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


"""
init_sqlite_db 
ID(INT): user telegram id
NAME(TEXT): telegram nick name
GREETINGS_TYPE(TEXT): greetings type
GREETINGS_TIME(DATETIME): greetings time
"""


def init_sqlite_db():
    try:
        # sqlite connect
        conn = sqlite3.connect('goodnight_bot.db')
        logger.info("Opened database successfully")
        conn.execute(
            '''
            CREATE TABLE GOODNIGHT_LIST
               (ID                    INTEGER       PRIMARY KEY ,
               NAME                   TEXT                      ,
               GREETINGS_TYPE         TEXT                      ,
               DATE                   TEXT                      ,
               TIME                   TEXT                              
               );
            '''
        )
        logger.info("Table init successfully")
        conn.close()
    except Exception as exception:
        logger.error(exception)


def update_user(from_id, send_name, greetings_type):
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    now_time = time.strftime("%H:%M:%S", time.localtime())
    # sqlite connect
    try:
        conn = sqlite3.connect('goodnight_bot.db')
        cur = conn.cursor()
        logger.info("Opened database successfully")
        sql = (
            '''
            REPLACE INTO 'GOODNIGHT_LIST' (
            'ID', 'NAME', 'GREETINGS_TYPE', 
            'DATE', 'TIME'
            )
            VALUES (?, ?, ?, ?, ?);
            '''
        )
        para = (from_id, send_name, greetings_type,
                now_date, now_time)
        cur.execute(sql, para)
        conn.commit()
        conn.close()
        # logger.debug(sql, para)
        logger.info("db update complete.")
    except Exception as exception:
        logger.error(exception)


def select_user_one(from_id):
    result = None
    try:
        conn = sqlite3.connect('goodnight_bot.db')
        cur = conn.cursor()
        logger.info("Opened database successfully")
        sql = (
            '''
            select ID,
            NAME,
            GREETINGS_TYPE,
            DATE,
            TIME 
            from GOODNIGHT_LIST
            WHERE ID=?
            '''
        )
        cur.execute(sql, (from_id,))
        result = cur.fetchall()[0]
    except Exception as exception:
        logger.error(exception)
    return result


def calculate_sleeping_interval(result):
    if result is not None:
        if len(result) > 0:
            ID = result[0]
            NAME = result[1]
            GREETINGS_TYPE = result[2]
            DATE: str = result[3]
            TIME: str = result[4]
            time_string: str = "" + DATE + " " + TIME
            interval = (datetime.now() - datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S"))
            return interval


init_sqlite_db()


@bot.message_handler(content_types=["document", "audio", "photo", "sticker", "audio"])
def echo(message):
    logger.debug(message)


try:
    @bot.message_handler(commands=["greeting"])
    def greeting(message):
        greetings_type = get_time_type()
        send_name, from_id = get_sender_name_and_id(message)

        # if not reply to anyone
        if message.reply_to_message is None:
            if greetings_type == "睡觉":
                update_user(from_id, send_name, greetings_type)
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
            elif greetings_type == "早安":
                result = select_user_one(from_id)
                interval = calculate_sleeping_interval(result)
                if interval is not None:
                    if interval < timedelta(hours=12):
                        greetings_type = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～她昨晚一共睡了 {interval} 哦～".format(
                            send_name=send_name,
                            from_id=from_id,
                            txt=greetings_type,
                            interval=interval - timedelta(microseconds=interval.microseconds),
                        )
                    else:
                        greetings_type = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～但离上次打卡已经超过12小时了哦～".format(
                            send_name=send_name,
                            from_id=from_id,
                            txt=greetings_type,
                        )
                else:
                    greetings_type = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～但昨晚忘记了打卡～".format(
                        send_name=send_name,
                        from_id=from_id,
                        txt=greetings_type,
                    )
                bot.send_message(message.chat.id, greetings_type, parse_mode="Markdown")
            else:
                greetings_type = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～".format(
                    send_name=send_name,
                    from_id=from_id,
                    txt=greetings_type,
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
                    update_user(from_id, send_name, greetings_type)
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
            greetings_type = get_time_type()
            update_user(from_id, send_name, greetings_type)
            if greetings_type == "睡觉":
                update_user(from_id, send_name, greetings_type)
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

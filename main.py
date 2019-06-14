#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("/usr/local/python3.6/lib/python3.6/site-packages")
sys.path.append("/usr/local/lib/python3.5/dist-packages")
import telebot
import json
import time
import random
from telebot import types

# read config from config.json
with open('./config.json', 'r+') as config_file:
    config = json.load(config_file)
    print('Config file load successfully:\n' + str(config))
    bot_token = config['bot_token']

# bot token
bot = telebot.TeleBot(bot_token)

# custom nickname by detect userID
custom_userid = [400521524, 407635222, 223347749, 638996316, 299143063, 459094099, 254030480, 73322551]
custom_nickname = ['小熊', 'Lore酱', '47', '47', '荔枝', 'mashiro', 'KingCapri', '柯柯']
random_stickers = ['CAADBQADvgYAAvjGxQoD_y6N-wJ3BwI', 'CAADBQADOAYAAvjGxQrGnfgTD5nfwQI']
sleep_reminder = ['您还没有睡觉吗？', '快去睡觉了啦！', '她已经睡着了喔…', '对方已经是守夜冠军了！', '你这么寂寞的嘛…', '[Google搜索：失眠怎么办](https://www.google.com/search?q=失眠怎么办)']

try:
	@bot.message_handler(commands=['greeting'])
	def greeting(message):
		# get local time
		c_time = time.time() + 28800
		c_time = int(c_time % 86400 // 3600)

		# change greeting text depend on time
		if 0<=c_time<4:
			txt = "睡觉"
		elif 4<=c_time<11:
			txt = "早安"
		elif 11<=c_time<14:
			txt = "中午好"
		elif 14<=c_time<18:
			txt = "下午好"
		elif 18<=c_time<22:
			txt = "晚上好"
		elif 22<=c_time<24:
			txt = "晚安"

		# if nickname recorded
		if message.from_user.id in custom_userid:
			send_name = custom_nickname[custom_userid.index(message.from_user.id)]
		else:
			send_name = str(message.from_user.first_name)

		from_id = str(message.from_user.id)

		# if not reply to anyone
		if message.reply_to_message == None:
			txt = "[" + send_name + "](tg://user?id=" + from_id + ") 向 大家 道 " + txt + "～"
			bot.send_message(message.chat.id, txt, parse_mode="Markdown")
		else:
			# if it is a reply message
			# if nickname recorded
			if message.reply_to_message.from_user.id in custom_userid:
				reply_name = custom_nickname[custom_userid.index(message.reply_to_message.from_user.id)]
			else:
				reply_name = str(message.reply_to_message.from_user.first_name)
			reply_id = str(message.reply_to_message.from_user.id)
			if txt == "早安":
				randNum = random.randint(0, 100)
				if randNum % 6 == 0:
					bot.send_sticker(message.chat.id, "CAADBQADGgUAAvjGxQrFBpd8WnW-TwI")
					txt = "[" + reply_name + "](tg://user?id=" + reply_id + ")～ [" + send_name + "](tg://user?id=" + from_id + ") 爱你哦～"
				else:
					txt = "[" + send_name + "](tg://user?id=" + from_id + ") 向 [" + reply_name + "](tg://user?id=" + reply_id + ") 道 " + txt + "～"
				# send reply and delete command message
				bot.reply_to(message.reply_to_message, txt, parse_mode="Markdown")
			if txt == "睡觉":
				randReminder = random.randint(0, len(sleep_reminder) - 1)
				txt = sleep_reminder[randReminder]
				# send reply and delete command message
				bot.reply_to(message.reply_to_message, txt, parse_mode="Markdown")
			else:
				randNum = random.randint(0, 100)
				if randNum % 6 == 0:
					randStick = random.randint(0, len(random_stickers) - 1)
					bot.send_sticker(message.chat.id, random_stickers[randStick])
				txt = "[" + send_name + "](tg://user?id=" + from_id + ") 向 [" + reply_name + "](tg://user?id=" + reply_id + ") 道 " + txt + "～"
				# send reply and delete command message
				bot.reply_to(message.reply_to_message, txt, parse_mode="Markdown")
		# bot.delete_message(message.chat.id, message.message_id)

	bot.polling(none_stop=True)
# catch exception
except KeyboardInterrupt:
    quit()
except Exception as e:
    print(str(e))

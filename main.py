#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("/usr/local/python3.6/lib/python3.6/site-packages")
sys.path.append("/usr/local/lib/python3.5/dist-packages")
import telebot
import time
from telebot import types

# read config from config.json
with open('./config.json', 'r+') as config_file:
    config = json.load(config_file)
    print('Config file load successfully:\n' + str(config))
    bot_token = config['bot_token']

# bot token
bot = telebot.TeleBot(bot_token)

# custom nickname by detect userID
custom_userid = [400521524, 407635222, 223347749, 638996316, 299143063, 459094099]
custom_nickname = ['小熊', 'Lore酱', '47', '47', '荔枝', 'Yunhao']

try:
	@bot.message_handler(commands=['greeting'])
	def greeting(message):
		# get local time
		c_time = time.time() + 28800
		c_time = int(c_time % 86400 // 3600)

		# change greeting text depend on time
		if 0<=c_time<5:
			txt = "晚安"
		elif 5<=c_time<11:
			txt = "早上好"
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

		# if not reply to anyone
		if message.reply_to_message == None:
			txt = send_name + " 向 大家 道" + txt + "～"
		else:
			# if it is a reply message
			# if nickname recorded
			if message.reply_to_message.from_user.id in custom_userid:
				reply_name = custom_nickname[custom_userid.index(message.reply_to_message.from_user.id)]
			else:
				reply_name = str(message.reply_to_message.from_user.first_name)
			# if reply_to user doesn't have username
			if message.reply_to_message.from_user.username == None:
				txt = send_name + " 向 " + reply_name + " 道 " + txt + "～"
			# if you reply to yourself
			elif message.from_user.id == message.reply_to_message.from_user.id:
				txt = "我 给 我 自 己 打 招 呼" 
			# if you reply to the bot
			elif message.reply_to_message.from_user.username == "goodnight_prpr_bot":
				txt = "不需要 给窝 道 打招呼 啦～" 
			# common reply
			else:
				txt = send_name + " 向 " + reply_name + " 道 " + txt + "～ @" + message.reply_to_message.from_user.username
		# send reply and delete command message
		bot.send_message(message.chat.id, txt)
		bot.delete_message(message.chat.id, message.message_id)

	bot.polling(none_stop=True)
# catch exception
except KeyboardInterrupt:
    quit()
except Exception as e:
    print(str(e))

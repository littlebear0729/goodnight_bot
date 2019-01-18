#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("/usr/local/python3.6/lib/python3.6/site-packages")
sys.path.append("/usr/local/lib/python3.5/dist-packages")
import telebot
import time
from telebot import types

# bot token
bot = telebot.TeleBot("REPLACE YOUR TOKEN HERE")

# custom nickname by detect userID
custom_userid = [400521524, 407635222, 223347749, 638996316, 299143063, 459094099]
custom_nickname = ['小熊', 'Lore酱', '47', '47', '荔枝', 'Yunhao']

try:
	@bot.message_handler(commands=['greeting'])
	def greeting(message):

		# if nickname recorded
		if message.from_user.id in custom_userid:
			send_name = custom_nickname[custom_userid.index(message.from_user.id)]
		else:
			send_name = str(message.from_user.first_name)

		# if not reply to anyone
		if message.reply_to_message == None:
			txt = send_name + " 向 大家 拜年啦！"
		else:
			# if it is a reply message
			# if nickname recorded
			if message.reply_to_message.from_user.id in custom_userid:
				reply_name = custom_nickname[custom_userid.index(message.reply_to_message.from_user.id)]
			else:
				reply_name = str(message.reply_to_message.from_user.first_name)
			# if reply_to user doesn't have username
			if message.reply_to_message.from_user.username == None:
				txt = send_name + " 向 " + reply_name + " 拜年啦！"
			# if you reply to yourself
			elif message.from_user.id == message.reply_to_message.from_user.id:
				txt = "我 给 我 自 己 拜 年" 
			# if you reply to the bot
			elif message.reply_to_message.from_user.username == "goodnight_prpr_bot":
				txt = "同喜同喜 同乐同乐！" 
			# common reply
			else:
				txt = send_name + " 向 " + reply_name + " 拜年啦！ @" + message.reply_to_message.from_user.username
		# send reply and delete command message
		bot.send_message(message.chat.id, txt)
		bot.delete_message(message.chat.id, message.message_id)

	bot.polling(none_stop=True)
# catch exception
except KeyboardInterrupt:
    quit()
except Exception as e:
    print(str(e))

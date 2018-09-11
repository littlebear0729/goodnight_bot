#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("/usr/local/python3.6/lib/python3.6/site-packages")
sys.path.append("/usr/local/lib/python3.5/dist-packages")
import telebot
import time
from telebot import types


bot = telebot.TeleBot("REPLACE YOUR TOKEN HERE")
group_id = open("group_id", "r").read().split()

@bot.message_handler(commands=['greeting'])
def greeting(message):
	print(message.chat.id)
	if str(message.chat.id) in group_id:
		c_time = time.time() + 28800
		c_time = int(c_time % 86400 // 3600)
		if 0<=c_time<4:
			txt = "晚安"
		elif 4<=c_time<10:
			txt = "早上好"
		elif 10<=c_time<15:
			txt = "中午好"
		elif 15<=c_time<18:
			txt = "下午好"
		elif 18<=c_time<21:
			txt = "晚上好"
		elif 21<=c_time<24:
			txt = "晚安"
		send_name = str(message.from_user.first_name)
		if message.reply_to_message == None:
			txt = send_name + "向大家道" + txt + "～"
		else:
			reply_name = str(message.reply_to_message.from_user.first_name)
			txt = send_name + "向" + reply_name + "道" + txt + "～ @" + message.reply_to_message.from_user.username
		bot.send_message(message.chat.id, txt)
		bot.delete_message(message.chat.id, message.message_id)


bot.polling()

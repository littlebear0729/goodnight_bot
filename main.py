#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import telebot
from telebot import types


token = open("config", "r").read()
group_id = open("group_id", "r").read().split()

bot = telebot.Telebot("token")

@bot.message_handler(commands=['goodnight'])
def goodnight(message):
	print(message.chat.id)
	#print(message)
	if str(message.chat.id) in group_id:
		if message.reply_to_message == None:
			txt = str(message.from_user.first_name)
			txt = txt + "向大家道晚安~"
			bot.send_message(message.chat.id, txt)
		else:
			txt = str(message.from_user.first_name)
			txt = txt + "向" + str(message.reply_to_message.from_user.first_name) + "道晚安~"
			bot.send_message(message.chat.id, txt)


bot.polling()
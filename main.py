#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import telebot
from telebot import types


token = open("config", "r").read()
group_id = open("group_id", "r").read().split()
group_mates = open("group_mates", "r").read().split()



'''bot = telebot.Telebot("token")'''

@bot.message_handler(commands=['goodnight'])
def goodnight(message):
	if message.chat.id in group_id:
	txt = "晚安"
	for i in range(0, len(group_mates)):
		txt = txt + "@" + group_mates[i] + " "
	bot.reply_to(message, txt)



bot.polling()
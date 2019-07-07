#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
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
custom_userid = [400521524, 407635222, 223347749, 638996316, 299143063, 459094099, 254030480, 73322551, 137105537, 557153656, 239887702]
custom_nickname = ['小熊', 'Lore酱 | ☆可爱 verified by LittleBear', '47', '47', '荔枝', 'mashiro', 'KingCapri', '柯柯', '成本', '妹抖喵喵喵喵', 'Yooooooru']
random_stickers = ['CAADBQADvgYAAvjGxQoD_y6N-wJ3BwI', 'CAADBQADOAYAAvjGxQrGnfgTD5nfwQI']
sleep_reminder = ['小可爱还没有睡觉吗？', '快去睡觉了啦！', '她已经睡着了喔…', '你的小可爱已经是守夜冠军了！']

def get_time():
	# get local time
	c_time = time.time() + 28800
	c_time = int(c_time % 86400 // 3600)
	# change greeting text depend on time
	if 0<=c_time<4:
		txt = '睡觉'
	elif 4<=c_time<11:
		txt = '早安'
	elif 11<=c_time<14:
		txt = '中午好'
	elif 14<=c_time<18:
		txt = '下午好'
	elif 18<=c_time<22:
		txt = '晚上好'
	elif 22<=c_time<24:
		txt = '晚安'
	return txt

def get_sender_name_and_id(message):
	if message.from_user.id in custom_userid:
		send_name = custom_nickname[custom_userid.index(message.from_user.id)]
	else:
		send_name = str(message.from_user.first_name)

	from_id = str(message.from_user.id)
	return send_name, from_id

def get_reply_name_and_id(message):
	# if nickname recorded
	if message.reply_to_message.from_user.id in custom_userid:
		reply_name = custom_nickname[custom_userid.index(message.reply_to_message.from_user.id)]
	else:
		reply_name = str(message.reply_to_message.from_user.first_name)
	reply_id = str(message.reply_to_message.from_user.id)
	return reply_name, reply_id

@bot.message_handler(content_types=['document', 'audio', 'photo', 'sticker', 'audio'])
def echo(message):
	print(message)

try:
	@bot.message_handler(commands=['greeting'])
	def greeting(message):
		txt = get_time()
		send_name, from_id = get_sender_name_and_id(message)

		# if not reply to anyone
		if message.reply_to_message == None:
			if txt == '睡觉':
				randNum = random.randint(0, 100)
				if randNum % 5 == 0:
					bot.send_message(message.chat.id, '下面我宣布！[{send_name}](tg://user?id={from_id}) 是守夜冠军啦！'.format(send_name=send_name, from_id=from_id), parse_mode="Markdown")
					bot.send_document(message.chat.id, 'CgADBQADkAADdcmxV9tAyTZinfacAg')
					txt = '晚安'
				else:
					txt = '晚安'
			txt = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～".format(send_name=send_name, from_id=from_id, txt=txt)
			bot.send_message(message.chat.id, txt, parse_mode="Markdown")
		else:
			# if it is a reply message
			if not message.from_user.id == message.reply_to_message.from_user.id and not message.reply_to_message.from_user.username == "goodnight_prpr_bot":
				reply_name, reply_id = get_reply_name_and_id(message)
				if txt == "早安":
					randNum = random.randint(0, 100)
					if randNum % 5 == 0:
						bot.send_sticker(message.chat.id, 'CAADBQADGgUAAvjGxQrFBpd8WnW-TwI')
						txt = "[{reply_name}](tg://user?id={reply_id})～ [{send_name}](tg://user?id={from_id}) 爱你哦～".format(reply_name=reply_name, reply_id=reply_id, send_name=send_name, from_id=from_id)
					else:
						txt = "[{send_name}](tg://user?id={from_id}) 向 [{reply_name}](tg://user?id={reply_id}) 道 {txt}～".format(send_name=send_name, from_id=from_id, reply_name=reply_name, reply_id=reply_id, txt=txt)
						# send reply and delete command message
						bot.reply_to(message.reply_to_message, txt, parse_mode="Markdown")
				elif txt == "睡觉":
					randNum = random.randint(0, 100)
					if randNum % 5 == 0:
						randReminder = random.randint(0, len(sleep_reminder) - 1)
						txt = sleep_reminder[randReminder]
					else:
						txt = "[{send_name}](tg://user?id={from_id}) 向 [{reply_name}](tg://user?id={reply_id}) 道 晚安～".format(send_name=send_name, from_id=from_id, reply_name=reply_name, reply_id=reply_id)
					# send reply and delete command message
					bot.reply_to(message.reply_to_message, txt, parse_mode="Markdown")
				else:
					randNum = random.randint(0, 100)
					if randNum % 5 == 0:
						randStick = random.randint(0, len(random_stickers) - 1)
						bot.send_sticker(message.chat.id, random_stickers[randStick])
					txt = "[{send_name}](tg://user?id={from_id}) 向 [{reply_name}](tg://user?id={reply_id}) 道 {txt}～".format(send_name=send_name, from_id=from_id, reply_name=reply_name, reply_id=reply_id, txt=txt)
					# send reply and delete command message
					bot.reply_to(message.reply_to_message, txt, parse_mode="Markdown")
		# bot.delete_message(message.chat.id, message.message_id)
	

	@bot.inline_handler(func=lambda query: True)
	def query_text(inline_query):
		try:
			print(inline_query)
			send_name, from_id = get_sender_name_and_id(inline_query)
			txt = get_time()
			if txt == '睡觉':
				txt = '晚安'
			txt1 = "[{send_name}](tg://user?id={from_id}) 向 大家 道 {txt}～".format(send_name=send_name, from_id=from_id, txt=txt)
			greeting1 = types.InlineQueryResultArticle('1', '向大家问好', types.InputTextMessageContent(txt1, parse_mode="Markdown"))
			if len(inline_query.query) != 0:
				if inline_query.query[0] == '@':
					txt2 = "{send_name} 向 {reply_name} 道 {txt}～".format(send_name=send_name, reply_name=inline_query.query, txt=txt)
					greeting2 = types.InlineQueryResultArticle('2', '向{reply_name}问好'.format(reply_name=inline_query.query), types.InputTextMessageContent(txt2))
					bot.answer_inline_query(inline_query.id, [greeting1, greeting2], cache_time=0, is_personal=False)
			else:
				bot.answer_inline_query(inline_query.id, [greeting1], cache_time=0, is_personal=False)
		except Exception as e:
			print(e)
	
	bot.polling(none_stop=True)
# catch exception
except KeyboardInterrupt:
    quit()
except Exception as e:
    print(str(e))

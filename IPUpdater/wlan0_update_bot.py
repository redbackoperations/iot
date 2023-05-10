import os

import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')

filepath = os.path.join("/home/pi/IPInfo", "wlan0.txt")

with open(filepath) as file:
        ip = file.readline()

file.close()

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

message = "Latest wlan0 IP config for Redback Pi 0000001: " + ip

bot.send_message(-1001950776693, message)

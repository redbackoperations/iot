import os
import telebot
from dotenv import load_dotenv, set_key
import subprocess

env_path = '/home/pi/.env'
load_dotenv(env_path)

#get bot token and device ID
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEVICE_ID = os.environ.get('DEVICE_ID')

#create telegram bot instance 
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

#get existing IPs
curr_eth0 = os.environ.get('ETH0_IP')
curr_wlan0 = os.environ.get('WLAN0_IP')

#get most recent ETH0 IP
with open('eth0_temp.txt') as file:
        new_eth0 = file.readline()

file.close()
subprocess.run("rm eth0_temp.txt", shell=True)

#get most recent WLAN0 IP
with open('wlan0_temp.txt') as file:
        new_wlan0 = file.readline()

file.close()
subprocess.run("rm wlan0_temp.txt", shell=True)

#check if eth0 IP has changed and if necessary update env record and send telegram alert
if new_eth0 != curr_eth0:
        set_key(env_path, 'ETH0_IP', new_eth0)
        message = "Latest eth0 IP config for Redback Pi" + str(DEVICE_ID) + ": " + new_eth0
        bot.send_message(-1001950776693, message)

#check if eth0 IP has changed and if necessary update env record and send telegram alert
if new_wlan0 != curr_wlan0:
        set_key(env_path, 'WLAN0_IP', new_wlan0)
        message = "Latest wlan0 IP config for Redback Pi" + str(DEVICE_ID) + ": " + new_eth0
        bot.send_message(-1001950776693, message)

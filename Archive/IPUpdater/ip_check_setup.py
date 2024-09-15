from dotenv import set_key
bot_token_input = input("Enter Bot Token:\n")

env_path = '/home/pi/.env'

set_key(env_path, 'BOT_TOKEN', str(bot_token_input))
set_key(env_path, 'ETH0_IP', " ")
set_key(env_path, 'WLAN0_IP', " ")
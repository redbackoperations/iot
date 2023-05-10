echo "Enter BOT Token:"
read bot_token

if [ -d "home/pi/IPInfo"]; then
	rm -r /home/pi/IPInfo
fi

mkdir /home/pi/IPInfo
touch /home/pi/IPInfo/eth0.txt
touch /home/pi/IPInfo/wlan0.txt
touch /home/pi/IPInfo/BOT_TOKEN.txt
echo $bot_token > /home/pi/IPInfo/BOT_TOKEN.txt

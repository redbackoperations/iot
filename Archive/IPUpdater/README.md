# Raspberry Pi IP Address Update Bot

## Purpose

Given that there is not a static IP address for the Pi and some users need to access the Pi remotely via SSH and the Deakin VPN, a way of keeping track of the IP address was needed. 
To accomplish this, we have created a Telegram Bot and a group. Via the scripts within this repository, the IP of the Pi can be checked every 10 minutes and if it has been changed a new message will be sent to the Telegram group allowing participants to see the new IP.

## Deployment on new Linux Install

### Step 1
Run the command below to install the pyTelegramBotAPI
```
pip install pyTelegramBotAPI
```

### Step 2
Clone the repository and run the script "ip_check_setup.py". Please have your bot token ready to enter when prompted. Do not add any spaces before or after the token.
```
python3 ip_check_setup.py
```

### Step 3
Run the following code to make the IP check script executable:
```
chmod +x check_ip.sh
```
Should this return an error, run the command as sudo as per the below:
```
sudo chmod +x check_ip.sh
```

### Step 4
You will need to add the script to a cron schedule to run every 10 minutes. This can be done by first running
```
crontab -e
```

Once in the editor, append the below to the cron schedule. Note: change the file path if needed.
```
*/10 * * * * /home/iot/IPUpdater/check_ip.sh
```
After this the script will be run every 10 minutes and, if need be, an updated IP will be sent to the Telegram group.

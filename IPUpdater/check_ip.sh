ifconfig eth0 | grep 'inet' > eth0_temp.txt
ifconfig wlan0 | grep 'inet' > wlan0_temp.txt

curr_eth0=$(head -1 eth0.txt)
new_eth0=$(head -1 eth0_temp.txt)

curr_wlan0=$(head -1 wlan0.txt)
new_wlan0=$(head -1 wlan0_temp.txt)

rm eth0_temp.txt
rm wlan0_temp.txt

if [ "$curr_eth0" != "$new_eth0" ]; then
        echo "$new_eth0" > eth0.txt
        python3 eth0_update_bot.py
fi

if [ "$curr_wlan0" != "$new_wlan0" ]; then
        echo "$new_wlan0" > wlan0.txt
        python3 wlan0_update_bot.py
fi

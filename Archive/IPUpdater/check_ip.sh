ifconfig eth0 | grep 'inet' > eth0_temp.txt
ifconfig wlan0 | grep 'inet' > wlan0_temp.txt

new_eth0=$(head -1 eth0_temp.txt)
rm eth0_temp.txt
echo $new_eth0 > eth0_temp.txt

new_wlan0=$(head -1 wlan0_temp.txt)
rm wlan0_temp.txt
echo $new_wlan0 > wlan0_temp.txt

python3 ip_updater.py
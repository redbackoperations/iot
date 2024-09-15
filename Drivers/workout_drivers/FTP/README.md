# Using this FTP test:

## Setting up:
Make sure the kickr is online,and connected to the pi via the 'start_kickr.sh' script and the hardware is running/sending data, as these scripts depend on values being received via the bike/device/power topic
(Can use publish_tester.py script on a windows machine to manually publish power data)

## Run
run 'python3 FTP_workout.py' in the Drivers/FTP/ directory.
The default minute duration is 20 minutes, add a command line arg after the script to set minutes
example :  python3 FTP_workout.py 2 (sets duration to 2 minutes)

## Troubleshooting
- if you're not sure if any MQTT messages are being sent and received, run the subscriber.py this should listen for messages from the power topic

## Running the publish_tester.py script
- run the publish_tester in a different window, press spacebar to enter a numeric value which will publish to power topic
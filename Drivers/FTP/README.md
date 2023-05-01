### Using this FTP test:

## Setting up:
Make sure the kickr is connected to the pi and running/sending data, as these scripts (except for the publish tester) depend on values being received via the bike/device/power topic
run 'python3 test_workout.py' and select the duration option

## To do as of 01.05.2023  (Remove when completed )
- Implement scripts that call the 'FTP_Workout.py' file, we want to use the environment variables from the pi for MQTT configuration and should replace using the test_workout.py program
- using the FTP_workout script should be the same as the test_workout, but at this time due to the .env config variables not being read properly, to get a workable feature we run the test_workout with hardcoded MQTT creds.

## Troubleshooting
- if you're not sure if anything is working, run the subsciber.py this should listen for messages from the power topic
- run the publish_tester in a different window, press spacebar to enter a numeric value which will publish to power topic (can also run ftp workout scripts and use publish tester to write values to the workout)
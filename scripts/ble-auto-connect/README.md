# BLE Auto Connecting Script

[Image of script running to be inserted]

This script was created to handle some persistent BLE issues we had with the bike. Connecting to the bike was not consistent with failed pairing on start up and even manually connecting using the `bluetoothctl` interface on the Raspberry Pi not working consistently. This script should resolve these issues by using `bluetoothctl` and `expect` script to act like a user and automatically resolve the BLE connection.

## Script Start & Setup

To start this script run the following command from the home directory: 

`bash iot/scripts/ble-auto-connect/ble_auto_connect.sh`

### KICKR MAC Address

The KICKR's MAC address must be accurately stored in the hidden `.env` file, in the home directory, with the following format:

`... KICKR_MAC_ADDRESS="XX:XX:XX:XX:XX:XX" ...`

*To access the hidden environment file use `nano .env` in the home directory*

### Bike on Standby

Ensure that the bike is not on standby: the BLE indicator light on the KICKR is blink blue and not off

[Image to be inserted]

*If it is on standby rotate the pedals a few times*

### Expect Installed

Ensure `expect` is installed using:

`sudo apt-get install expect`

## Script Process

[Flow chart of scripts decision logic to be inserted]

The script follows a simple flow of commands reacting to expected outputs to terminal from `bluetoothctl` commands and writing input commands into the terminal.

### Once Started

Once the script has been started, it enter commands into the terminal interface like a user, waiting for expected output from commands and responding to resolve any issues. 

[Image of script process to be inserted]

**DO NOT** attempt to enter anything into command-line during this process - if you must, terminate the script using `Ctrl + C` before doing so.

### Script Completion

If a connection was successfully achieved, an output to the terminal should indicate so:

`Connection established with bike via BLE`

[Image to be inserted]

### Script Failure

The above process should only take a few seconds but can fail for unknown reasons and enter into a loop. If this happens, use `Ctrl + C` to terminate the script and then restart both the bike & Pi, and re-run the script.

## Future

Some improvements to the script are desireable and left for future team members to implement:

- Running the script on Pi start up using a daemon to fully automate the connection
- Running the script on script start up (`start_all.sh`) so that BLE connection is always resolved before other processes initialise
- Running the script in a background process so that it does not interfer with the command-line
- Forever looping the script so that it will reconnect if the connection drops for some reason
- Extend script to handle any future encountered issues
- Change the regex pattern used to match the KICKR MAC address to be more forgiving

## Resources

- `bluetoothctl` - https://manpages.debian.org/unstable/bluez/bluetoothctl.1.en.html
- `expect` introduction - https://phoenixnap.com/kb/linux-expect
- Reading files using `tcl` (the backbone of `expect`) - https://wiki.tcl-lang.org/page/How+do+I+read+and+write+files+in+Tcl
- Shell script & expect script located in `iot/scripts/ble_auto_connect.sh`
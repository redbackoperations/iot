#!/bin/bash

# auto connect to the bike by resolving the BLE issues automatically via bluetoothctl
source ~/.env
echo "Attempting auto connect to bike via BLE"

# set target MAC address
TARGET_ADDRESS=$KICKR_MAC_ADDRESS

EXPECT_SCRIPT="ble_auto_connect.exp"
expect "$EXPECT_SCRIPT"

echo "Connection established with bike via BLE"

exit 0
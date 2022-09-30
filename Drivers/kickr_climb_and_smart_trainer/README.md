# BLE Control for Wahoo Kickr Smart Trainer and Wahoo Kickr Climb

### This driver is capable of controlling both resistance and inclination for Wahoo Kickr Smart Trainer and Wahoo Kickr Climb devices.

---

## Prerequisites

1. This driver is tested in a **Linux OS environment** - Raspberry Pi 4 Model B. It doesn't work in MacOS due to some missing packages. Most probably, it won't work for Windows either. So a **Linux OS environment** is needed to run this driver.

2. Please follow the [gatt-python](https://github.com/getsenic/gatt-python) module's README to install all of the necessary dependencies.

3. Ensure you have `systemctl`, `bluez`, `gattctl`, `bluetoothctl` and `python3-dbus` installed already.

4. Please also make sure you have installed [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) module: `pip install paho-mqtt`.

5. To test out this driver, you will need a MQTT broker setup at [HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/)

6. A BLE fitness hardware device with Fitness Machine Service (FTMS) support is also needed to test this driver. Alternatively, you can create a virtual BLE device using a BLE development tool, such as [LightBlue App](https://apps.apple.com/us/app/lightblue/id557428110).

## Usage

1. Ensure the fitness hardware device has been turned on and waiting for BLE pairing.

2. In a Linux terminal, run either `sudo gattctl --discover` or `./Drivers/lib/ble_devices_scan.py` (under the `iot` Git repo) to scan BLE devices, and find out the exact MAC address for the fitness hardware device you're going to interact with.

3. Under the `iot` Git repo, run the following command with proper BLE and MQTT connection arguments to initiate the driver for incline and resistance control:

```
./Drivers/kickr_climb_and_smart_trainer/incline_and_resistance_control.py --mac_address "THE_WAHOO_KICKR_PRODUCT_BLUETOOTH_MAC_ADDRESS"  --broker_address="HIVEMQ_CLOUD_MQTT_BROKER_ADDRESS_HERE" --username="HIVEMQ_CLOUD_USERNAME_HERE" --password="HIVEMQ_CLOUD_PASSWORD_HERE" --resistance_command_topic=bike/000001/resistance/control --incline_command_topic=bike/000001/incline/control --resistance_report_topic=bike/000001/resistance --incline_report_topic=bike/000001/incline
```

4. If the BLE and MQTT connections are built correctly, you should now see some logs as the following:

```
Connecting to the BLE device...
[2b:80:03:12:bf:dd] Resolved services
[2b:80:03:12:bf:dd]	Service [0000fab0-0000-1000-8000-00805f9b34fb]
...
CONNACK received with code Success.
Subscribed: 1 [<paho.mqtt.reasoncodes.ReasonCodes object at 0xb4fece50>, <paho.mqtt.reasoncodes.ReasonCodes object at 0xb4fdaec8>]
...
```

5. Connect to your MQTT broker using either a MQTT CLI tool or a MQTT UI tool. And subscribe to the MQTT command and command report topics, such as `bike/000001/resistance/control` and `bike/000001/resistance`.

6. You can now publish a MQTT message to the corresponding command topic (e.g., `bike/000001/resistance/control` or `bike/000001/incline/control`) with a `text/plain` payload like: `-10` for incline or `100` for resistance.

7. From the terminal log, you will see a MQTT command message has been received and it's sent to the BLE FTMS control point for resistance control or the custom Characteristic control point for incline control to assign the new value:

```
...
[MQTT message received for Topic: 'bike/000001/incline', QOS: 0]  -10
Trying to set a new inclination value: -10
Requesting FTMS control...
A new value has been written to 00002ad9-0000-1000-8000-00805f9b34fb
A new value has been written to 00002ad9-0000-1000-8000-00805f9b34fb
A new value has been written to 00002ad9-0000-1000-8000-00805f9b34fb
A new inclination has been set successfully: -10
...
```

8. From the MQTT broker interface you've connected before, since a new resistance/incline value has been set, you will see a new command report with the newly assigned value coming up to the subscribed command report topic, such as `bike/000001/resistance` or `bike/000001/incline`.

## Helpful Resources

The official Bluetooth specification docs relating to BLE Fitness devices can be found in the followings:

- https://www.thisisant.com/assets/resources/Datasheets/D00001699_-_GFIT_User_Guide_and_Specification_Document_v2.0.pdf
- https://www.bluetooth.com/specifications/specs/fitness-machine-service-1-0/
- https://www.bluetooth.com/specifications/specs/gatt-specification-supplement-6/

Here're some helpful docs relating to MQTT module usages in Python:

- http://www.steves-internet-guide.com/loop-python-mqtt-client/
- https://github.com/eclipse/paho.mqtt.python

Here're some helpful resources about 1) how BLE devices to be connected via GATT protocol and 2) how to control Bluetooth FTMS features, such as resistance and inclination:

- https://www.youtube.com/watch?v=AokDN6r4iz8
- https://github.com/Berg0162/simcline/tree/master/Wahoo%20Kickr/
- https://stormotion.io/blog/how-to-integrate-ble-fitness-devices-into-app/
- https://docs.microsoft.com/en-us/windows/uwp/devices-sensors/gatt-client#perform-readwrite-operations-on-a-characteristic
- https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt
- https://github.com/getsenic/gatt-python

A full sample log about using this driver to interact with a [Yesoul Smart Bike](https://www.yesoul.net/bike/m1) can be found under this path: `/Drivers/kickr_climb_and_smart_trainer/sample_logs/ftms_service_and_characteristic_read_sample_1.log`.

# Description:
This device interacts with the wahoo kickr and climbr via the Raspberry Pi 000001, located in the IoT lab, building M.102.
Its intention is to manipulate the hardware in real-time without the need for running or accessing third-party software such as the mobile app, VR, or other interfaces.
The purpose of this is that it allows users to simply use the bike with a simple interface.

# How to Run:
- Kickr script (/iot/scripts/./start_kickr.sh) must be executed and successful connection between Pi and Kickr must be established for this device to work as intended.
- Turn on remote device by pushing the white button on the power regulator on the top of the breadboard
- BT module should be flashing red while waiting for pairing.
- Navigate to iot/Drivers/pico_remote and execute the script via 'python3 pico_bt_handler.py' to run the handler.
- successful connection is determined by the HC-06 module turning into a solid red light.
- Upon successful connection between the HC-06 Bluetooth module and the Raspberry pi, you may now interact with the hardware via the push buttons:

### Note: You must press and hold the selected button in order to influence hardware.

# Buttons:
### Button 1: increase resistance
### Button 2: decrease resistance
### Button 3: increase incline
### Button 4: decrease incline

![Screenshot 2023-09-24 142627](https://github.com/redbackoperations/iot/assets/69894063/d3f90db2-0b68-41e7-b8c1-3ca8d65c8ad4)
![WIN_20230924_12_03_43_Pro](https://github.com/redbackoperations/iot/assets/69894063/0cd708ff-146f-48b0-ac11-f858ef215387)
![WIN_20230924_12_03_08_Pro](https://github.com/redbackoperations/iot/assets/69894063/91f63b5b-432b-4208-a054-40ffb96bd527)


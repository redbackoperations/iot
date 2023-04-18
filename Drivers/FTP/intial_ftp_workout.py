import time
import keyboard
import os
from mqtt_client import MQTTClient

def message(client, userdata, msg):
	power = int(str(msg.payload.decode("utf-8")))
	if power < 0 or power > 100:
		print(f"Invalid power in message: {msg}")
		return
	return power


# Conduct the 2 minute FTP test
# NOTE: This function will be updated to 20 minutes, for testing purposes it is 2 minutes, 
# so that the test doesn't take too long

def perform_ftp_test():
    global received_power
    test_duration = 2 * 60  # 20 minutes in seconds
    start_time = time.time()
    power_data = []
    current_power = 0
    
    while time.time() - start_time < test_duration:
        received_power = message 
        power_data.append(current_power)
        time.sleep(1) 
        print("Current power: ", current_power)
        print("Current time: ", time.time() - start_time)
        
        #Keyboard interrupt to stop the test:
        if(keyboard.is_pressed('q')):
            print("Test stopped")
            return power_data
    return power_data

# Calculate FTP from the test data
def calculate_ftp(power_data):
    avg_power = sum(power_data) / len(power_data)
    ftp = avg_power * 0.95  # Multiply the average power by 0.95 for the 20-minute test
    return ftp

def main():
    try:
        global mqtt_client
        global deviceId
        mqtt_client = MQTTClient(os.getenv('MQTT_HOSTNAME'), \
            os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
        mqtt_client.setup_mqtt_client()
        deviceId = os.getenv('DEVICE_ID')
        mqtt_client.subscribe(f"bike/{deviceId}/kickr/power")
        
        mqtt_client.get_client().on_message = message
        mqtt_client.get_client().loop_start()
        
        print("Starting the 20-minute FTP test...")
        power_data = perform_ftp_test()
        ftp = calculate_ftp(power_data)
        print(f"Your estimated FTP is: {ftp:.2f} watts")

    except KeyboardInterrupt:
        print("Test stopped")
        pass
    
    mqtt_client.get_client().loop_stop()
    
if __name__ == "__main__":
    main()
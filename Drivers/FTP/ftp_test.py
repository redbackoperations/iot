import time
import serial
import keyboard

# Establish a connection to the power meter or smart trainer
def connect_power_meter():
    return
    # THis will either be used to require MQTT readings from cadence tracker or to connect to a power meter
    # For now, we will just use a keyboard input to simulate the power meter
    
## TO DO ##
# Read power data from the connected device and change this method when we connect MQTT or the power meter
def read_power_data(power):
    if(keyboard.is_pressed('w')):
        power += 5
    if (keyboard.is_pressed('s')):
        power -= 5
    power = max(0, power)
    return power

# Conduct the 2 minute FTP test
# NOTE: This function will be updated to 20 minutes, for testing purposes it is 2 minutes, 
# so that the test doesn't take too long

def perform_ftp_test():
    test_duration = 2 * 60  # 20 minutes in seconds
    start_time = time.time()
    power_data = []
    current_power = 0
    
    while time.time() - start_time < test_duration:
        current_power = read_power_data(current_power)
        power_data.append(current_power)
        time.sleep(1) 
        print("Current power: ", read_power_data(current_power))
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
    print("Starting the 20-minute FTP test...")
    power_data = perform_ftp_test()
    ftp = calculate_ftp(power_data)
    print(f"Your estimated FTP is: {ftp:.2f} watts")

if __name__ == "__main__":
    main()
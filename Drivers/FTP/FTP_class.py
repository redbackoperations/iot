import time

class FTP():
    def __init__(self):
        self.duration = 0
        self.power_data = [0]
        self.ftp = 0
        
    def perform_ftp_test(self):
        # 20 minutes in seconds
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                time.sleep(1)
                if(self.power_data != None): 
                    print("Current power: ", self.power_data[-1])
                    print("Current time: ", time.time() - start_time)
                else:
                    print("No power data received")

        except KeyboardInterrupt:
            print("Test stopped")
            print("Count of data points given: " + str(len(self.power_data)))
            pass

    def calculate_ftp(self):
        avg_power = sum(self.power_data) / len(self.power_data)
        ftp = avg_power * 0.95  # Multiply the average power by 0.95 for the 20-minute test
        return ftp

    def message(self, client, userdata, msg):
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        self.power_data.append(int(msg.payload.decode("utf-8")))

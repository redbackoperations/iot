import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import json
from mqtt_client import MQTTClient

# Global variables for GUI
resistance_var = None
incline_var = None
speed_var = None
distance_var = None
power_var = None  # Declare power_var as a global variable
countdown_var = None  # Declare countdown_var as a global variable
heartbeat_rate_var = None
rpm_var = None

# Global variables for simulation
training_active = False
countdown_active = False
start_time = 0
distance_traveled = 0

def start_training():
    global training_active, countdown_active, start_time, distance_traveled
    if not training_active:
        training_active = True
        countdown_active = True
        start_time = time.time()  # Record the start time of pedaling
        distance_traveled = 0  # Reset distance traveled
        countdown_timer()

def stop_training():
    global training_active, countdown_active, start_time, distance_traveled
    if training_active:
        training_active = False
        countdown_active = False
        start_time = 0  # Reset the start time
        distance_traveled = 0  # Display Distance Traveled
        speed_var.set("0 m/s")  # Reset speed display
        distance_var.set("0.00 km")  # Reset distance display
        countdown_var.set("5:00")  # Reset the countdown display

def countdown_timer():
    global countdown_active
    if countdown_active:
        remaining_time = 300 - int(time.time() - start_time)
        if remaining_time <= 0:
            stop_training()
            return
        countdown_var.set(f"{remaining_time // 60}:{remaining_time % 60:02}")
        calculate_distance(float(speed_var.get().split()[0]))
        root.after(1000, countdown_timer)
    else:
        countdown_var.set("5:00")  # Reset the countdown display
        
        
def reset_values():
    global training_active, countdown_active, start_time, distance_traveled
    training_active = False
    countdown_active = False
    start_time = 0  # Reset the start time
    distance_traveled = 0  # Display Distance Traveled
    speed_var.set("0 m/s")  # Reset speed display
    distance_var.set("0.00 km")  # Reset distance display
    countdown_var.set("5:00")  # Reset the countdown display
    resistance_var.set("0 %")
    incline_var.set("0 %")
    rpm_var.set("0 RPM")
    power_var.set("0 Watts")
    heartbeat_rate_var.set("0 BPM")    
    
    
def read_message(client, userdata, msg):
    # Get power data from MQTT
    print("message received")
    print(msg.payload)
    
    if msg.topic == f'bike/000001/power':
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        power_payload = msg.payload.decode('utf-8')
        try:   
            dict_of_power_payload = json.loads(power_payload)
            power = dict_of_power_payload['value']
        except json.JSONDecodeError:
            power = power_payload
        power_var.set(f"{power} Watts")
        
    # Get speed data from MQTT
    if msg.topic == f'bike/000001/speed':
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        speed_payload = msg.payload.decode('utf-8')
        try:
            dict_of_speed_payload = json.loads(speed_payload)
            speed = dict_of_speed_payload["value"]
        except json.JSONDecodeError:
            speed = speed_payload
            
       # calculate_distance(speed)
        speed = str(round(speed, 2))
        speed_var.set(f"{speed} m/s")

    if msg.topic == f'bike/000001/cadence':
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        rpm_payload = msg.payload.decode('utf-8')
        try:
            dict_of_rpm_payload = json.loads(rpm_payload)
            rpm = dict_of_rpm_payload["value"]
        except json.JSONDecodeError:
            rpm = rpm_payload
        rpm_var.set(f"{rpm} RPM")
    
    if msg.topic == f'bike/000001/incline/control':
        incline_payload = msg.payload.decode('utf-8')
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        incline_var.set(f"{incline_payload} %")
    
    if msg.topic == f'bike/000001/resistance/control':
        resistance_payload = msg.payload.decode('utf-8')
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        resistance_var.set(f"{resistance_payload} %")
        
    # Get Heartrate Data from MQTT
    if msg.topic == f'bike/000001/heartrate':
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        heart_payload = msg.payload.decode('utf-8')
        try:
            dict_of_heart_payload = json.loads(heart_payload)
            heart = dict_of_heart_payload["value"]
        except json.JSONDecodeError:
            heart = heart_payload
            
        heartbeat_rate_var.set(f"{heart} BPM")

def calculate_distance(speed):
    global start_time, distance_traveled

    current_time = time.time()
    elapsed_time = current_time - start_time
    # Calculate distance traveled based on speed and elapsed time
    distance_traveled += speed * elapsed_time / 10000  # Convert meters to kilometers
    dist = str(round(distance_traveled, 2))
    distance_var.set(f"{dist} km")

def main():
    global root, resistance_var, heartbeat_rate_var, incline_var, speed_var, distance_var, rpm_var, power_var, countdown_var
    try: 
        global mqtt_client
        global deviceId
    # Initialize MQTT client and subscribe to speed topic
        mqtt_client = MQTTClient(('f5b2a345ee944354b5bf1263284d879e.s1.eu.hivemq.cloud'), ('redbackiotclient'), ('IoTClient@123'))
        topic1 = f'bike/000001/speed'
        topic2 = f'bike/000001/power'
        topic3 = f'bike/000001/heartrate'
        topic4 = f'bike/000001/cadence'
        topic5 = f'bike/000001/resistance/control'
        topic6 = f'bike/000001/incline/control'
        
        mqtt_client.setup_mqtt_client()
        print(topic1)
        print(topic2)
        print(topic3)
        print(topic4)
        print(topic5)
        print(topic6)
        mqtt_client.subscribe(topic1)
        mqtt_client.subscribe(topic2)
        mqtt_client.subscribe(topic3)
        mqtt_client.subscribe(topic4)
        mqtt_client.subscribe(topic5)
        mqtt_client.subscribe(topic6)
        
        mqtt_client.get_client().on_message = read_message
        mqtt_client.get_client().loop_start()

    except KeyboardInterrupt:
        pass

    root = tk.Tk()
    root.title("Smart Indoor Bike Dashboard")
    root.geometry("1200x700+100+50")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Background Image
    bg_image = Image.open("cycling_background_v2.jpg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0)
    
    # Create left and right frames
    left_frame = ttk.Frame(root, width= 500, height=800, padding="10 10 10 10")
    left_frame.pack(side="left", expand=True, fill=tk.NONE, padx=5, pady=100)
    
    right_frame = ttk.Frame(root, width= 500, height=800, padding="10 10 10 10")
    right_frame.pack(side="right", expand=True, fill=tk.NONE, padx=5, pady=100)
    
    # Resistance Label and Entry
    resistance_label = tk.Label(left_frame, text="Resistance:", font=("Helvetica", 20, "bold"))
    resistance_var = tk.StringVar()
    resistance_var.set("0 %")
    resistance_value_label = tk.Label(left_frame, textvariable=resistance_var, font=("Helvetica", 16))
    
    resistance_label.pack(pady=10)
    resistance_value_label.pack()
    
    # Incline Label and Entry
    incline_label = tk.Label(left_frame, text="Incline:", font=("Helvetica", 20, "bold"))
    incline_var = tk.StringVar()
    incline_var.set("0 %")
    incline_value_label = tk.Label(left_frame, textvariable=incline_var, font=("Helvetica", 16))
    
    incline_label.pack(pady=10)  
    incline_value_label.pack() 

    # Power Label
    power_label = tk.Label(left_frame, text="Power:", font=("Helvetica", 20, "bold"))
    power_var = tk.StringVar()
    power_var.set("0 Watts")
    power_value_label = tk.Label(left_frame, textvariable=power_var, font=("Helvetica", 16))

    power_label.pack(pady=10)
    power_value_label.pack()

    # Speed Label
    speed_label = tk.Label(left_frame, text="Speed:", font=("Helvetica", 20, "bold"))
    speed_var = tk.StringVar()
    speed_var.set("0 m/s")
    speed_value_label = tk.Label(left_frame, textvariable=speed_var, font=("Helvetica", 16))
    
    speed_label.pack(pady=10)
    speed_value_label.pack()

    #RPM Label
    rpm_label = tk.Label(left_frame, text="RPM:", font=("Helvetica", 20, "bold"))
    rpm_var = tk.StringVar()
    rpm_var.set("0 RPM")
    rpm_value_label = tk.Label(left_frame, textvariable=rpm_var, font=("Helvetica", 16))

    rpm_label.pack(pady=10)
    rpm_value_label.pack()
    
    
    # Heartbeat Rate Label
    heartbeat_rate_label = tk.Label(right_frame, text="Heartrate:", font=("Helvetica", 20, "bold"))
    heartbeat_rate_var = tk.StringVar()
    heartbeat_rate_var.set("0 BPM")
    heartbeat_value_label = tk.Label(right_frame, textvariable=heartbeat_rate_var, font=("Helvetica", 16))
    
    heartbeat_rate_label.pack(pady=10)
    heartbeat_value_label.pack(pady=10)
    
    
    # Distance Label
    distance_label = tk.Label(right_frame, text="Distance:", font=("Helvetica", 20, "bold"))
    distance_var = tk.StringVar()
    distance_var.set("0.00 km")
    distance_value_label = tk.Label(right_frame, textvariable=distance_var, font=("Helvetica", 16))
    distance_label.pack(pady=10)
    distance_value_label.pack()

    # Countdown Label
    countdown_label = tk.Label(right_frame, text="Timer:", font=("Helvetica", 20, "bold"))
    countdown_var = tk.StringVar()
    countdown_value_label = tk.Label(right_frame, textvariable=countdown_var, font=("Helvetica", 16))
    countdown_label.pack(pady=10)
    countdown_value_label.pack()
    
    # Start Button
    start_button = ttk.Button(right_frame, text="START TIMER", command=start_training, width=20)
    start_button.pack(pady=10)
    
    # Stop Button
    stop_button = ttk.Button(right_frame, text="STOP TIMER", command=stop_training, width=20)
    stop_button.pack(pady=10)
    
    # Reset all Values
    reset_button = ttk.Button(right_frame, text="RESET ALL VALUES", command=reset_values, width=20)
    reset_button.pack(pady=10)

    # root.after(1000, update_values)  # Start the update loop
    root.mainloop()
    
    mqtt_client.get_client().loop_stop()
if __name__ == "__main__":
    main()


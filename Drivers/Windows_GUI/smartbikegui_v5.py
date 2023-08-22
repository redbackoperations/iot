import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import paho.mqtt.client as mqtt

# Global variables for GUI
resistance_var = None
incline_var = None
speed_var = None
distance_var = None

# Global variables for simulation
training_active = False
start_time = 0
distance_traveled = 0

# MQTT client setup
mqtt_client = mqtt.Client()

def on_message(client, userdata, message):
    # Handle incoming MQTT message here
    # Update resistance, incline, or other parameters based on the received message
    pass

mqtt_client.on_message = on_message

def setup_mqtt():
    mqtt_client.connect("mqtt_broker_address", 1883)
    mqtt_client.subscribe("topic/resistance")
    mqtt_client.subscribe("topic/incline")
    mqtt_client.loop_start()

def update_values():
    global start_time, distance_traveled

    if training_active:
        # Get the current time
        current_time = time.time()

        # Calculate elapsed time since the user started pedaling
        elapsed_time = current_time - start_time

        # Simulate speed based on resistance and incline levels (replace with actual logic)
        resistance = int(resistance_var.get())
        incline = int(incline_var.get())
        speed = resistance + incline  # This is just a simple example, adjust as needed

        # Calculate distance traveled based on speed and elapsed time
        distance_traveled = speed * elapsed_time / 3600  # Convert seconds to hours

        # Update GUI with calculated values
        speed_var.set(f"{speed} km/h")
        distance_var.set(f"{distance_traveled:.2f} km")

        # Publish current resistance and incline values to MQTT topics
        mqtt_client.publish("topic/resistance", resistance)
        mqtt_client.publish("topic/incline", incline)

    # Schedule the next update after a delay (in milliseconds)
    root.after(1000, update_values)

# Rest of the code remains unchanged
# ...

def main():
    global root, resistance_var, incline_var, speed_var, distance_var, resistance_entry, incline_entry

    root = tk.Tk()
    root.title("Smart Indoor Bike Dashboard")

      # Background Image
    bg_image = Image.open("cycling_path.jpg")
    bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0)

    # Resistance Label and Entry
    resistance_label = tk.Label(root, text="Resistance:", font=("Helvetica", 16))
    resistance_label.place(x=30, y=30)
    resistance_var = tk.StringVar()
    resistance_var.set(5)  # Default value for resistance
    resistance_entry = ttk.Entry(root, textvariable=resistance_var, font=("Helvetica", 16))
    resistance_entry.place(x=170, y=30)
    resistance_entry.bind("<Return>", on_resistance_change)

    # Incline Label and Entry
    incline_label = tk.Label(root, text="Incline:", font=("Helvetica", 16))
    incline_label.place(x=30, y=70)
    incline_var = tk.StringVar()
    incline_var.set(5)  # Default value for incline
    incline_entry = ttk.Entry(root, textvariable=incline_var, font=("Helvetica", 16))
    incline_entry.place(x=170, y=70)
    incline_entry.bind("<Return>", on_incline_change)

    # Speed Label
    speed_label = tk.Label(root, text="Speed:", font=("Helvetica", 16))
    speed_label.place(x=30, y=120)
    speed_var = tk.StringVar()
    speed_value_label = tk.Label(root, textvariable=speed_var, font=("Helvetica", 16))
    speed_value_label.place(x=170, y=120)

    # Distance Label
    distance_label = tk.Label(root, text="Distance:", font=("Helvetica", 16))
    distance_label.place(x=30, y=160)
    distance_var = tk.StringVar()
    distance_value_label = tk.Label(root, textvariable=distance_var, font=("Helvetica", 16))
    distance_value_label.place(x=170, y=160)

    # Start Button
    start_button = ttk.Button(root, text="START", command=start_training)
    start_button.place(x=50, y=210)

    # Stop Button
    stop_button = ttk.Button(root, text="STOP", command=stop_training)
    stop_button.place(x=150, y=210)

    setup_mqtt()  # Setup MQTT after creating the root window

    root.after(1000, update_values)  # Start the update loop

    root.mainloop()

if __name__ == "__main__":
    main()


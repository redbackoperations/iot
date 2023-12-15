import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

def on_connect(client):
    client.subscribe("Button/Test")
    print("Connected")

def ButtonTest():
    state = GPIO.input(11)
    if state == 1:
        print('HIGH')
    else:
        print('LOW')
    client.publish("Button/Test", str(state))
    



if __name__=="__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("broker.emqx.io", 1883, 60)
    try:
        while True:
            ButtonTest()
            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()
    

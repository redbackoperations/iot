import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

R_TURN = 11
L_TURN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(R_TURN, GPIO.IN)
GPIO.setup(L_TURN, GPIO.IN)

def on_connect(client):
    client.subscribe("Button/Test")
    print("Connected")

def ButtonTest():
    R_State = GPIO.input(R_TURN)
    L_State = GPIO.input(L_TURN)
    if R_State == 1:
        print('RIGHT')
        client.publish("Turn/Right", "RIGHT")
    elif R_State == 0:
        print('R_LOW')
        client.publish("Turn/Right", "LOW")
        
    if L_State == 1:
        print('LEFT')
        client.publish("Turn/Left", "LEFT")
    elif L_State == 0:
        print('L_LOW')
        client.publish("Turn/Left", "LOW")
    
    



if __name__=="__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("broker.emqx.io",1883,10)
    try:
        while True:
            ButtonTest()
            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()  
        client.disconnect()
    

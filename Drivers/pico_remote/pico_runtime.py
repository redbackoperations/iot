from machine import Pin, UART
import utime

# Assume button is connected to GPIO pin 15
button = Pin(2, Pin.IN, Pin.PULL_UP)

# Configure UART communication
uart = UART(1, 9600)
cntr = 0
while True:
    if button.value() == 0:  # When button is pressed
        cntr += 1
        uart.write('Button Pressed\n')
        print('Button Pressed: ', cntr)
        utime.sleep_ms(300)  # Debounce delay
################## WARNING ##################
# naming this file to main.py and storing it on the pico without any safety backup to return to the REPL will result in
# bricking the pico pi, as the pico will boot straight into main.py at startup and become unresponsive to connectio attempts from
# the Thonny IDE from that point forward.

# Absolute mandatory to perform thorough testing of implementation with naming file to anything other than 'main.py'.
# Only once going to production naming this file to main.py and flashing to pico will be necessary to boot this program on start-up

###############################################


from machine import Pin, UART
import utime


increase_button = Pin(2, Pin.IN, Pin.PULL_UP)
decrease_button = Pin(15, Pin.IN, Pin.PULL_UP)

# Configure UART communication
# We use Port TX/RX 1 between pico and pi at baudrate 9600

uart = UART(1, 9600)

while True:
    if increase_button.value() == 0:  # When button is pressed
        uart.write('increase\n')
        print('Increase Button Pressed: ')
        utime.sleep_ms(1000)  # Debounce delay
        
    if decrease_button.value() == 0:  # When button is pressed
        uart.write('decrease\n')
        print('Decrease Button Pressed: ')
        utime.sleep_ms(1000)  # Debounce delay
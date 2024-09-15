################## WARNING ##################
# naming this file to main.py and storing it on the pico without any safety backup to return to the REPL will result in
# bricking the pico pi, as the pico will boot straight into main.py at startup and become unresponsive to connectio attempts from
# the Thonny IDE from that point forward.

# Absolute mandatory to perform thorough testing of implementation with naming file to anything other than 'main.py'.
# Only once going to production naming this file to main.py and flashing to pico will be necessary to boot this program on start-up

###############################################


from machine import Pin, UART
import utime


increase_resistance_button = Pin(19, Pin.IN, Pin.PULL_UP)
decrease_resistance_button = Pin(18, Pin.IN, Pin.PULL_UP)
increase_incline_button = Pin(17, Pin.IN, Pin.PULL_UP)
decrease_incline_button = Pin(16, Pin.IN, Pin.PULL_UP)
# Configure UART communication
# We use Port TX/RX 1 between pico and pi at baudrate 9600

uart = UART(1, 9600)

while True:
    if increase_resistance_button.value() == 0:  # When button is pressed
        uart.write('increaseResistance\n')
        print('Increase resistance Button Pressed: ')
        utime.sleep_ms(1000)  # Debounce delay
        
    if decrease_resistance_button.value() == 0:  # When button is pressed
        uart.write('decreaseResistance\n')
        print('Decrease resistance Button Pressed: ')
        utime.sleep_ms(1000)  # Debounce delay
        
    if increase_incline_button.value() == 0:  # When button is pressed
        uart.write('increaseIncline\n')
        print('Increase incline Button Pressed: ')
        utime.sleep_ms(1000)  # Debounce delay
        
    if decrease_incline_button.value() == 0:  # When button is pressed
        uart.write('decreaseIncline\n')
        print('Decrease incline Button Pressed: ')
        utime.sleep_ms(1000)  # Debounce delay
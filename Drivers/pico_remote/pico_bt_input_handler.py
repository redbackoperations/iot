import bluetooth

hc06_address = " 98:D3:51:FE:68:16"
port = 1

print("Connecting to HC-06...")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((hc06_address, port))

sock.send("Hello from Raspberry Pi!")
print("Connected, waiting for data")

buffer = " "
try:
    while True:
            data = sock.recv(1024).decode('utf-8')
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                print("Receieved: " + line.strip())
except KeyboardInterrupt:
    print("Closing socket")
    
sock.close()
print("Done")
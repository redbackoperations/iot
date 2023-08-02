import bluetooth

hc06_address = "98:D3:31:40:60:B0"
port = 1


print("Connecting to socket..")
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((hc06_address, port))

sock.send("Hello Pico")
print("Connected, waiting for data")
buffer = " "
try:
    while True:
        data = sock.recv(1024).decode('utf-8')
        buffer += data
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            print("Received:", line.strip())
except KeyboardInterrupt:
    print("Closing connection")

sock.close()
print("Connection closed")

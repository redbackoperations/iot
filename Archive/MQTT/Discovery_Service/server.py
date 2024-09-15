import socket
import struct

BROADCAST_PORT = 1096
RESPONSE_PORT = 1097
BIKE_ID = "000001"


# get_ip_address - Return the ip address of the current machine
# params - None
# returns - IPv4 address of the current machine (string in dotted notation)
def get_ip_address():
    return socket.gethostbyname(socket.gethostname())


# create_broadcast_payload - Create the broadcast payload
# params - ip - The ip address of the client (machine creating the broadcast)
# returns - payload to broadcast (msglen / 0000h / ipaddress)
def create_broadcast_payload(ip):
    parts = ip.split('.')
    return struct.pack('>HHBBBB',8,0,int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))


# create_response_payload - Create the response payload
# params - ip - The ip address of the server (machine sending the response)
#        - bikeId - The bikeId as a string
# returns - payload for the response (msglen / 0001h / ipaddress / bikeId)
def create_response_payload(ip, bikeId):
    parts = ip.split('.')
    bike = bikeId.encode('UTF-8')
    return struct.pack(f'>HHBBBB{len(bike)}s',8+len(bikeId),1,int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]),bike)


# receive_broadcast - Wait for a broadcast on the given address
# params - ip - the ip address to listen on
#        - port - the port to receive the broadcast
# returns - payload - the payload
#         - clientaddress - the ip address of the client sending the broadcast
# Create a socket and listen for a response, then return it and the ip address of the client (without the port)
def receive_broadcast(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((ip, port))
    print(f'Listening for broadcast on {ip}:{port}')
    payload, clientaddress = sock.recvfrom(256)
    sock.close()
    return payload, clientaddress[0]



# validate_broadcast - Check wether the broadcast is valid
# params - the payload to validate
#        - the ip address of the client sending the broadcast
# returns True if the broadcast is valid
# A valid response will have 8 characters, a command of 0, ip address matching the broadcasting machine
def validate_broadcast(payload, client_address):
    expected = create_broadcast_payload(client_address)
    return payload == expected


# send_response - Send a response on the given port
# params - server_ip - The ip address for the server (machine creating the response)
#        - bikeId - this is the string containing the Bike's ID for the MQTT topic
#        - client_ip - The ip address for the client (machine receiving the response)
#        - port - The port to send the response
# returns - Nothing
# Create a response payload for the given ip address and bike
# Create a socket to send a UDP DGRAM broadcast and send the payload
# Log the response to the console
def send_response(server_ip, bikeId, client_ip, port):
    payload = create_response_payload(server_ip, bikeId)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('0.0.0.0', 0))
    sock.sendto(payload, (client_ip, port))
    sock.close()
    print(f'Sent response {payload} to {client_ip}:{port}')


def main():
    try:
        while True:
            server_ip = get_ip_address()
            payload, client_ip = receive_broadcast(server_ip, BROADCAST_PORT)
            if validate_broadcast(payload, client_ip):
                send_response(server_ip, BIKE_ID, client_ip, RESPONSE_PORT)
            else:
                print(f'Invalid broadcast: {payload} from {client_address}')
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
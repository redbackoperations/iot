import socket
import struct

BROADCAST_PORT = 1096
RESPONSE_PORT = 1097


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


# broadcast - Send a broadcast on the given port
# params - ip - The ip address for the client (machine creating the broadcast)
#        - port - The port to send the broadcast
# returns - Nothing
# Create a broadcast payload for the given ip address
# Create a socket to send a UDP DGRAM broadcast and send the payload
# Log the broadcast to the console
def broadcast(ip, port):
    payload = create_broadcast_payload(ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('0.0.0.0', 0))
    sock.sendto(payload, ('255.255.255.255', port))
    sock.close()
    print(f'Sent broadcast {payload}')


# receive_response - Wait for a response on the given address
# params - ip - the ip address to listen on
#        - port - the port to receive the response
# returns - payload - the payload
#         - clientaddress - the ip address of the server
# Create a socket and listen for a response, then return it and the ip address of the client (without the port)
def receive_response(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((ip, port))
    print(f'Listening for response on {ip}:{port}')
    payload, clientaddress = sock.recvfrom(256)
    sock.close()
    return payload, clientaddress[0]


# validate_response - Check whether the response is valid
# params - the payload to validate
#        - the ip address of the server sending the response
# returns True if the response is valid
# A valid response will have 8-28 characters, a command of 1, ip address matching the responding machine
def validate_response(payload, server_ip):
    if len(payload) <= 8 or len(payload) > 28:
        return False
    string_length = len(payload) - 8
    expected = create_response_payload(server_ip, payload[8:].decode('UTF-8'))
    return payload == expected 


def main():
    client_ip = get_ip_address()
    broadcast(client_ip, BROADCAST_PORT)
    payload, server_ip = receive_response(client_ip, RESPONSE_PORT)
    if (validate_response(payload, server_ip)):
        print(f'Bike {payload[8:]} is at {server_ip}')
    else:
        print(f'Invalid response {payload} from {server_ip}')


if __name__ == "__main__":
    main()
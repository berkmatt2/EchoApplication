import socket
import sys
import argparse

def echo_client(port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    message = input("<PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n")
    sock.sendto(message.encode(), server_address)
    newMessage, server_address = sock.recvfrom(2048)
    print(newMessage.decode())
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Server Socket')
    parser.add_argument('--port', action = "store", dest = "port", type=int, required=True)
    parser.add_argument('--host', action = "store", dest = "host", type = str, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    host = given_args.host
    echo_client(port, host)
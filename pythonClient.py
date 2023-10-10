import socket
import sys
import argparse

def echo_client(port, host):
    """echo_client function: takes as input a port int and a host string
    creates a socket object, sends a message to the server via the socket
    receives the same message back and then closes the connection"""
    
    #code for connecting the socket, takes a host and a port and creates a connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    
    #take a message as input and send it to the server via the socket
    message = input("enter some text: ")
    sock.sendto(message.encode(), server_address)
    
    #receive 2048 bytes from the serve, print it, and close the socket
    newMessage, server_address = sock.recvfrom(2048)
    print(newMessage.decode())
    sock.close()
    
    #code to get the inputs from BASH, use --port <port> --host <hostname> to run
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Server Socket')
    parser.add_argument('--port', action = "store", dest = "port", type=int, required=True)
    parser.add_argument('--host', action = "store", dest = "host", type = str, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    host = given_args.host
    echo_client(port, host)
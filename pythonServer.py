import socket
import sys
import argparse


def echo_server(port):
    """echo_server function: takes a port as input and creates
    a socket which listens for data. Upon receiving data the server
    sends the same message back to the client after printing it and
    then closes the socket"""
    
    #create the socket object and bind it to the port, begin listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("", port)
    sock.bind(server_address)
    sock.listen(5)
    
    #while loop which constantly listens for data on the given port
    while True:
        print("Waiting to receive message from client")
        client, address = sock.accept()
        data = client.recv(2048)
        
        #when data is received, print it out and then send it back, close the connection when done
        if data:
            print("Data: ", data.decode())
            client.send(data)
        client.close()
        
    #code for handling the inputs from BASH, --port <port int>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Socket Server')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
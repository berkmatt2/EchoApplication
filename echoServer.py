import socket
import sys
import argparse
import time

data_payload = 2048
backlog = 5

def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("", port)
    sock.bind(server_address)
    sock.listen(backlog)
    while True:
        print("Waiting to receive message from client")
        client, address = sock.accept()
        data = client.recv(data_payload)
        if data:
            message = data.decode()
            splitMsg = message.split()
            isValid = True
            if splitMsg[0] != "s":
                isValid = False
            if splitMsg[1] != "rtt" and splitMsg[1] != "tput":
                isValid = False
            if splitMsg[2].isnumeric():
                numProbes = int(splitMsg[2])
                if numProbes < 1:
                    isValid = False
            else:
                isValid = False
            if splitMsg[3].isnumeric():
                numBytes = int(splitMsg[3])
                if numBytes < 1:
                    isValid = False
            else:
                isValid = False
            servDelayStr = splitMsg[4]
            servDelayStr = servDelayStr[:-2]
            if servDelayStr.isnumeric():
                servDelay = int(servDelayStr)
                if servDelay < 0:
                    isValid = False
            else:
                isValid = False
                
            if isValid == True:
                measurementType = splitMsg[1]
                probes = numProbes
                size = numBytes
                delay = servDelay
                rtt(probes, delay, sock, server_address)
            else:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                
def rtt(numProbes, serverDelay, sock, server_address):
    probeNumber = 0
    delay = serverDelay / 1000
    client, address = sock.accept()
    response = "200 OK: Ready"
    client.send(response.encode())
    while True:
        data = client.recv(data_payload)
        if data:
            message = data.decode()
            splitMsg = message.split()
            newProbeNum = splitMsg[1]
            if newProbeNum == (probeNumber + 1) and newProbeNum <= numProbes:
                probeNumber += 1
                time.sleep(delay)
                client.send(data)
            else:
                message = "404 ERROR: Invalid Measurement Message"
                client.send(message.encode())
            if newProbeNum == numProbes:
                return
            
                
                
            
        
        
    
                
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Socket Server')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
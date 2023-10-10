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
            if " " in message:
                splitMsg = message.split()
            else:
                splitMsg = message
            print(splitMsg)
            if splitMsg[0] == "t":
                if splitMsg[:-2] == "t":
                    response = "200 OK: Closing Connection"
                    client.send(response.encode())
                else:
                    response = "404 ERROR: Invalid Connection Termination Message"
                    client.send(response.encode())
                client.close()
                sys.exit(0)
            isValid = True
            try:
                splitMsg[0]
            except IndexError:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                sys.exit(0)
            try:
                splitMsg[1]
            except IndexError:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                sys.exit(0)
            try:
                splitMsg[2]
            except IndexError:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                sys.exit(0)
            try:
                splitMsg[3]
            except IndexError:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                sys.exit(0)
            try:
                splitMsg[4]
            except IndexError:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                sys.exit(0)
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
                rtt(probes, delay, sock, server_address, client)
            else:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                
def rtt(numProbes, serverDelay, sock, server_address, client):
    probeNumber = 0
    delay = serverDelay / 1000
    response = "200 OK: Ready"
    client.send(response.encode())
    while True:
        completeMessage = ""
        while True:
            data = client.recv(35000)
            temp = data.decode()
            completeMessage += temp
            if "\n" in completeMessage:
                break
        
        #data = client.recv(35000)
        message = completeMessage
        splitMsg = message.split()
        newProbeNum = int(splitMsg[1])
        print(newProbeNum)
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
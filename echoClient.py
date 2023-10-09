import socket
import sys
import argparse
import time

def echo_client(port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    message = input("<PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n")    
    sock.sendto(message.encode(), server_address)
    newMessage, server_address2 = sock.recvfrom(2048)
    print(newMessage.decode())
    if newMessage.decode() == "200 OK: Ready":
        splitMsg = message.split()
        measureType = splitMsg[1]
        numProbes = int(splitMsg[2])
        msgSize = int(splitMsg[3])
        temp = splitMsg[4]
        delay = temp[:-2]
        if measureType == "rtt":
            totalTime = 0
            for i in (range(numProbes)):
                result = rtt(numProbes, msgSize, i + 1, sock, server_address)
                if result == -500:
                    print("404 ERROR: Invalid Measurement Message")
                    break
            totalTime += result
            roundTripTime = totalTime / numProbes
            print("Average RTT for ", numProbes, " Messages of Size ", msgSize, "With Server Delay ", delay, ": ", roundTripTime)
        if measureType == "tput":
            totalTime = 0
            for i in (range(numProbes)):
                result = rtt(numProbes, msgSize, i + 1, sock, server_address)
                if result == -500:
                    print("404 ERROR: Invalid Measurement Message")
                    break
                else:
                    totalTime += result
            roundTripTime = totalTime / numProbes
            throughput = (msgSize * 8 * 0.001) / roundTripTime
            print("Throughput for ", numProbes, " Messages of Size ", msgSize, "With Server Delay ", delay, ": ", throughput)
            

            
        
def rtt(numProbes, payloadSize, probeID, socket, server_address):
    protocolPhase = "m"
    payload = 's' * payloadSize
    probeIDString = str(probeID)
    message = str(protocolPhase + " " + probeIDString + " " + payload + "\n")
    print(message)
    startTime = time.time()
    socket.sendto(message.encode(), server_address)
    response, server_address2 = socket.recvfrom(2048)
    if response.decode() == "404 ERROR: Invalid Measurement Message":
        return -500
    endTime = time.time()
    totalTime = endTime - startTime
    return totalTime
    
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Server Socket')
    parser.add_argument('--port', action = "store", dest = "port", type=int, required=True)
    parser.add_argument('--host', action = "store", dest = "host", type = str, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    host = given_args.host
    echo_client(port, host)
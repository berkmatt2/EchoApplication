import socket
import sys
import argparse
import time

def echo_server(port):
    """echo_server: input: port is an integer representing a tcp port
    creates a socket and begins listening on the given port. The Server waits
    for a proper connection setup message from the client and returns Ready or ERROR to the client
    It then repeatedly echoes measuring messages back to the client in order to measure the RTT"""
    
    #create the socket and set it to listen on the given port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("", port)
    sock.bind(server_address)
    sock.listen(5)
    
    #while loop to continually listen for messages from the client
    while True:
        
        #receive data from the client
        print("Waiting to receive message from client")
        client, address = sock.accept()
        data = client.recv(2048)
        
        #when data is received, begin to parse the message
        if data:
            message = data.decode()
            if " " in message:      #check for spaces, if there are spaces, use the split() function to split at the space
                splitMsg = message.split()
            else:
                splitMsg = message  #if there are no spaces, keep the message the same
                
            #code to check if the received message was to terminate the connection    
            if splitMsg[0] == "t":      #if the first index of the string is the letter "t", that may indicate the user is trying to close the socket
                if splitMsg[:-2] == "t":    #make sure the the newline character is included for it to be a proper closing message
                    response = "200 OK: Closing Connection"     #respond with termination message
                    client.send(response.encode())
                else:
                    response = "404 ERROR: Invalid Connection Termination Message" #if not proper format, send error
                    client.send(response.encode())
                client.close()      #either way, close the connection and exit the program
                sys.exit(0)
                
            #series of try-catch messages:
                #these ensure that if any connection setup phase info is missing, we don't index out of bounds
                #should we get an index out of bounds when indexing the split message array, close the socket and exit
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
            #END TRY-CATCH SECTION
            
            
            isValid = True #isValid will ensure that the connection setup message was properly formatted
            
            #ensure that the correct protocol phase was received
            if splitMsg[0] != "s":
                isValid = False
                
            #ensure that there is a proper measurement type 
            if splitMsg[1] != "rtt" and splitMsg[1] != "tput":
                isValid = False
                
            #makes sure that the number of probes is numeric and is no less than 10
            if splitMsg[2].isnumeric():
                numProbes = int(splitMsg[2])
                if numProbes < 10:
                    isValid = False
            else:
                isValid = False
                
            #ensure that message size is numeric and is not less than 1
            if splitMsg[3].isnumeric():
                numBytes = int(splitMsg[3])
                if numBytes < 1:
                    isValid = False
            else:
                isValid = False
                
            #ensures the the server delay is numeric and not less than 0. Must cut off the newline character
            servDelayStr = splitMsg[4]
            servDelayStr = servDelayStr[:-2]
            if servDelayStr.isnumeric():
                servDelay = int(servDelayStr)
                if servDelay < 0:
                    isValid = False
            else:
                isValid = False
                
            #as long as the connection setup message passed all tests, store the values and call the function to measure
            if isValid == True:
                measurementType = splitMsg[1]
                probes = numProbes
                size = numBytes
                delay = servDelay
                rtt(probes, delay, sock, server_address, client)
                
            #if the connection setup message is invalid, report it back to the client and close the socket
            else:
                response = "404 ERROR: Invalid Connection Setup Message"
                client.send(response.encode())
                client.close()
                
                
                
def rtt(numProbes, serverDelay, sock, server_address, client):
    """rtt function: inputs: numProbes is the int number of probes being sent, serverDelay is an int (in ms)
    representing the amount of time to wait before echoing back the message, sock is a socket object, server_address is a tuple (port,host)
    client is socket object. The RTT function will continually wait for data and then reconstruct it. It will echo the 
    message back to the client and, given a nonzero serverDelay it will sleep before sending the message back"""
    
    probeNumber = 0     #initialize a variable to hold the number of probes the server has received
    delay = serverDelay / 1000  #change server delay from a whole number ms value to an equivalent decimal seconds 
    
    #send the OK response indicating the server is ready to accept measurement messages
    response = "200 OK: Ready"
    client.send(response.encode())
    
    while True:
        
        #code to handle truncated messages (large amounts of data)
        completeMessage = ""    #accumulator to hold message
        while True:         #continue receiving messages until told to stop
            data = client.recv(35000)   #receive the incoming data
            temp = data.decode()        #decode and store in temp
            completeMessage += temp     #rebuild the message piece by piece
            if "\n" in completeMessage: #if we reache the delimiter (newline), we are done
                break
        
        #split the message where there are spaces in order to isolate the probeID
        message = completeMessage
        splitMsg = message.split()
        newProbeNum = int(splitMsg[1])
        
        #print for debugging purposes: ensuring all probes are being received by server
        print(newProbeNum)
        
        #Check to be sure that the newly received probe has ID that is one more than the previous and that too many weren't sent
        if newProbeNum == (probeNumber + 1) and newProbeNum <= numProbes:
            probeNumber += 1        #increment number of received probes
            time.sleep(delay)       #if there is a delay, sleep for delay seconds
            client.send(data)       #send the data back to the client
            
        #if the too many probes were sent or they are out of order, send an ERROR
        else:
            message = "404 ERROR: Invalid Measurement Message"
            client.send(message.encode())
            
        #once we reach the desired number of probes, return to the echo_server function
        if newProbeNum == numProbes:
            return
            
    
    #code to handle input in BASH, --port <port int>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Socket Server')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
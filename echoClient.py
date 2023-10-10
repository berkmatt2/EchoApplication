import socket
import sys
import argparse
import time

def echo_client(port, host):
    """echo_client function: takes as input an int as port and a string as a host name
    client will continually ask for user input in the form of a proper protocol phase message
    upon receiving user input, the client sends the message to the server which then indicates if the
    message is of the proper format. If the format is correct, the client stores the values of the measurement
    type, number of probes to send, size of the messages, and the server delay value. It then calls the function to calculate
    the RTT and then determines whether or not to print the RTT or calculate throughput and print that"""
    
    #while loop to continually ask for user input as long as the connection hasn't been closed
    while True:
        
        #create the socket using the given port and host name, connect to the server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        sock.connect(server_address)
        
        #request user input, provides a format for the message as well as format for the quit message
        print("<PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n")
        print("or <PROTOCOL PHASE>\n to quit")
        message = input("Enter a command: ")
        
        #send the message to the server
        sock.sendto(message.encode(), server_address)
        
        #receive the status message from the server and print it out
        newMessage, server_address2 = sock.recvfrom(2048)
        print(newMessage.decode())
        
        #check the status message returned by the server
        #if the message is to close the connection , exit the program
        if newMessage.decode() == "200 OK: Closing Connection":
            sys.exit(0)
            
        #if the new message indicates the server is set up and ready, split the originally sent message
        #the message will be split along the white spaces and all inputted values will be stored descriptively
        elif newMessage.decode() == "200 OK: Ready":
            splitMsg = message.split()
            measureType = splitMsg[1]       #position 1 is the measurement type, rtt or tput
            numProbes = int(splitMsg[2])    #position 2 is how many probes will be sent
            msgSize = int(splitMsg[3])      #position 3 is an indicator of the size (in bytes) of messages to be sent
            temp = splitMsg[4]              #position 4 is the server delay, must first seperate newline character to cast as int
            delay = temp[:-2]
            
            #code for calculating RTT, rtt() function returns a time which is added to the other
            #times cumulatively
            totalTime = 0                   
            for i in (range(numProbes)):
                result = rtt(numProbes, msgSize, i + 1, sock, server_address)
                if result == -500:
                    print("404 ERROR: Invalid Measurement Message")
                    break
                totalTime += result
                
            #average the RTT, take the total time (total time for x probes) and divide by num probes    
            roundTripTime = totalTime / numProbes
            
            #based on measurement type, print the RTT or calculate the throughput and print that
            if measureType == "rtt":
                print("Average RTT for ", numProbes, " Messages of Size ", msgSize, "With Server Delay ", delay, ": ", roundTripTime)
            if measureType == "tput":
                throughput = (msgSize * 8 * 0.001) / roundTripTime
                print("Throughput for ", numProbes, " Messages of Size ", msgSize, "With Server Delay ", delay, ": ", throughput)
      
def rtt(numProbes, payloadSize, probeID, socket, server_address):
    """rtt functionL: inputs: numProbes is the number of probes to be sent, payloadSize is the size
    of the messages to be sent, probeID is the number of the probe being sent, socket is a socket object
    server_address is a tuple of (port, host). Compiles and sends message protocol messages to the server.
    Is repeatedly called until the required number of probes is sent. Returns the time it takes for one probe to
    go to the server and back"""
    
    #building the message:
    #protocol phase is alwsays m
    #payload: one char in python is one byte, so take an arbitrary char and duplicate it payloadSize times
    #probeIDString: the probe ID as a string
    #adds the newline as a delimiter to parse truncated messages
    protocolPhase = "m"
    payload = 's' * payloadSize
    probeIDString = str(probeID)
    message = str(protocolPhase + " " + probeIDString + " " + payload + "\n")
    
    #take a time stamp just before sending the message to start the "stopwatch"
    startTime = time.time()
    socket.sendto(message.encode(), server_address)
    
    #when messages are large they become truncated into multiple messages
    #completeMessage represents the fully "rebuilt" message
    completeMessage = ""
    while True:         #loop until otherwise told
        data, server_address2 = socket.recvfrom(35000) #receive from the server
        temp = data.decode()        #decode the data and store in a temp variable
        completeMessage += temp     #cumulatively add to completeMessage
        if "\n" in completeMessage: #once we reach our delimiter (newline), we are done
            break
        
    #take a timestamp of the ending time when the message has been fully received   
    endTime = time.time()
    
    #if the message received indicates an invalid message was sent, return -500 to echo_client    
    if completeMessage == "404 ERROR: Invalid Measurement Message":
        return -500
    
    #the total time taken is the start time to the end time, return it
    totalTime = endTime - startTime
    return totalTime
    
    
    
   #used to parse inputs, --port <port int> --host <host name> 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Server Socket')
    parser.add_argument('--port', action = "store", dest = "port", type=int, required=True)
    parser.add_argument('--host', action = "store", dest = "host", type = str, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    host = given_args.host
    echo_client(port, host)
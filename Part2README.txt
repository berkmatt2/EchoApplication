COMPILATION INSTRUCTIONS

For echoServer.py:

1. Ensure that you are in the directory containing pythonServer.py
2. Type "python echoServer.py --port <PORT NUMBER (int)>" without quotes and where <PORT NUMBER (int)> is an integer betweeen 58000-58999
3. The server should now be waiting for messages from the client

For echoClient.py:

1. Ensure that you are in the directory containing pythonClient.py
2. Type "python echoClient.py --port <PORT NUMBER (int)> --host <HOST NAME>" without quotes where <PORT NUMBER (int)> is the port the
	server is running on and <HOST NAME> is the name of the machine running the server program (i.e. csa3.bu.edu, localhost, etc.)
3. The client should display sample messages of what to enter next
4. To conduct measurements: type a message with the following format:
	<PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><PAYLOAD SIZE><WS><SERVER DELAY>\n
   In this message, protocol phase should be 's' without quotes where s indicates setup phase
   Measurement type is either 'rtt' or 'tput' without quotes depending on which you want to measure
   Number of Probes is an integer greater than or equal to 10
   Payload Size is an integer greater than 0
   Server Delay is an integer greater than or equal to 0
   Be sure to include the newline character (it is used as a delimiter)

5. After sending a setup message of the proper format, the client will send the proper measurement messages to the server, which are echo'd back
6. The Client will display a message with either an RTT measurement in miliseconds or a Throughput measurement in bytes per milisecond
7. To terminate the connection: <PROTOCOL PHASE>\n where <PROTOCOL PHASE> is 't' without quotes
8. The server should respond with 200: OK and close the connection
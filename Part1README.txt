COMPILATION INSTRUCTIONS

For pythonServer.py:

1. Ensure that you are in the directory containing pythonServer.py
2. Type "python pythonServer.py --port <PORT NUMBER (int)>" without quotes and where <PORT NUMBER (int)> is an integer betweeen 58000-58999
3. The server should now be waiting for messages from the client

For pythonClient.py:

1. Ensure that you are in the directory containing pythonClient.py
2. Type "python pythonClient.py --port <PORT NUMBER (int)> --host <HOST NAME>" without quotes where <PORT NUMBER (int)> is the port the
server is running on and <HOST NAME> is the name of the machine running the server program (i.e. csa3.bu.edu, localhost, etc.)
3. The client should ask for some text
4. Type any text and press enter. The same message should be displayed in the client window.
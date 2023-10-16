TCP Echo Application

A Python socket-based program. This application will measure either the RTT or
the throughput of various TCP packet sizes. It will also allow the user to specify
a server delay value which simulates a propagation delay. 

I have implemented two applications: one which uses the echoClient.py and echoServer.py files
and the other utilizes the pythonClient.py and pythonServer.py files.
-pythonClient and pythonServer exist as more of a test program for echoing messages
from a client to a server and back to the client.
-echoClient and echoServer are the actual program files. These function largely the same as the
above files but also implement a standardized messaging format as well as functions to measure
the RTT and throughput of a given message.

This README does not include instructions on running the programs. I have included two seperate
README files. part1README will give instructions on running pythonClient and pythonServer. 
part2README will give instructions on running the echoClient and echoServer files. I have also
included a PDF file called "EchoApplication Tests and Results" which is a writeup detailing my 
design and the various tests I ran on the two programs. It also includes data graphs detailing
the relationship between packet size and RTT, packet size and Throughput, server delay and RTT,
and server delay and throughput.

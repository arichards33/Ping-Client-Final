# Project 3: HTTP server

This project implements a UDP-based ping client that communicates with a UDP-based ping server, to test for packet loss and RTTs.

# Set Up

To run the program you will call the 'PingServer' file that will take a port number, a simulated loss rate, and an average delay as command line inputs per the below.

java PingServer --port=<port> [--loss_rate=<rate>] [--avg_delay=<delay>]

Then run the 'PingClient.py' file that take in the server IP address, the port (same as the server), the number of pings to send, the wait interval (in milliseconds) between each segment, and the timeout time (in milliseconds) in the below format.

python PingClient.py <server ip addr> <server port> <number of pings to send> <wait interval> <timeout>

# Files
PingClient.py
PingServer.java

# version

 version 1.0

# Author

Alex Richards

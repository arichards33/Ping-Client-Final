import sys
import socket
import time
import threading

class PingClient():

    def __init__(self, serverIP, port, count, period, timeout):
        self.serverIP = serverIP
        self.port = int(port)
        self.count = int(count)
        self.period = int(period)/1000
        self.timeout = float(timeout)/1000
        self.sequenceNumber = 1
        self.maxRTT = None
        self.minRTT = None
        self.avgRTT = None
        self.times = []
        self.received = 0
        self.elapsedTime = None

    def connect(self):
        #create an INET, datagram socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket = s
        s.settimeout(self.timeout) #set the timeout time in seconds based off the command line input
        t = threading.Timer(self.period, self.send) #separate the pings by the period input (in seconds)
        t.start()

#send message to ping server and recieve the reponse
    def send(self):
        self.isIP() #check that the serverIP is an actual IP
        self.startTime = (time.time())*1000
        totalStart = self.startTime #keep initial start time for segment 1 to be used for aggregate stats
        print "PING %s" % self.serverIP
        while self.sequenceNumber <= self.count:
            self.startTime = (time.time())*1000
            message = "PING %s: seq=%d time=%s ms\r\n" % (self.serverIP, self.sequenceNumber, self.startTime)
            self.serverSocket.sendto(message, (self.serverIP, self.port))
            try:
                data, address = self.serverSocket.recvfrom(2048)
                recieved = data.split(" ")
                if recieved[0] == "PING": #received a response from the server
                    self.endTime = (time.time())*1000
                    self.calcRTT()
                    response = "PONG %s: %s %.1f ms" % (address[0], recieved[2], self.RTT)
                    print response
                    self.received += 1 #keep track of how many responses are recieved for loss rate stats
                    self.sequenceNumber += 1
            except socket.timeout: #didn't recieve a responsn and the timeout time was reached to end the send
                self.endTime = (time.time())*1000
                self.calcRTT()
                print "Sending Error: Timeout"
                self.sequenceNumber += 1

        self.elapsedTime = self.endTime - totalStart #determine the total time from segment 1 to the last segment is returned
        self.serverSocket.close()
        self.statistics()

#determine the RTT per segment
    def calcRTT(self):
        self.RTT = (self.endTime - self.startTime)
        self.times.append(self.RTT)

#makes the final calculations for the total RTT from segment 1 to the last segment
    def finalCalc(self):
        self.maxRTT = max(self.times)
        self.minRTT = min(self.times)
        self.avgRTT = sum(self.times)/len(self.times)

#returns the aggregate statistics for all the segments after they have been sent
    def statistics(self):
        self.finalCalc()
        loss = ((float(self.sequenceNumber - 1) - self.received)/(self.sequenceNumber - 1)) * 100
        line1 = "\n--- %s ping statistics ---" % self.serverIP
        line2 = "%d transmitted, %d recieved, %d%% loss, time %.1fms" % ((self.sequenceNumber - 1), self.received, loss, self.elapsedTime)
        line3 = "rtt min/avg/max = %.1f/%.1f/%.1f ms" % (self.minRTT, self.avgRTT, self.maxRTT)
        print line1
        print line2
        print line3

#make sure that the serverIP is an actual IP address, i.e. turns "localhost" into an IP
    def isIP(self):
        try:
            socket.inet_aton(self.serverIP)
        except socket.error:
            self.serverIP = socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    serverIP = (sys.argv[1])
    port = (sys.argv[2])
    count = (sys.argv[3])
    period = (sys.argv[4])
    timeout = (sys.argv[5])
    pingClient = PingClient(serverIP, port, count, period, timeout)
    pingClient.connect()

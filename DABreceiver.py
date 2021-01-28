import array
import socket

from threading import Lock, Thread


class DABreceiver:

    packetCounter = 0
    list = []
    megaList = []
    lrpn = -1
    inTransmission = False


    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.mutex = Lock()


    def sockets(self):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)  # create a socket
        sock.bind((self.ip, self.port))  # bind the socket to the IP and port
        return sock


    def checkChecksum(self, string, givenChecksum):
        string = string.encode()
        bytes = array.array('b', string)
        checksum = 0
        for i in range(len(bytes)):
            checksum ^= bytes[i]
        checksum = hex(checksum)
        print('checksum receiver: ' + checksum + '\n')
        if(checksum[2:] == givenChecksum):
            return True
        return False

    def verifyFile(self, list, packetCounter):
        for x in range(packetCounter):
            if(list[x] == ''):
                print('file not complete, some packets went missing\n')
                return False
        return True

    def main(self):
        while True:
            self.mutex.acquire()
            try:
                data, addr = self.sockets().recvfrom(4096)  # receive data
                data = data.decode('utf-8')
                packetNumber = int(data[0])
                self.packetCounter += 1
                data = data[1:]
                print('new Packet: ' + data + '\n')
                if(packetNumber == 0):
                    self.inTransmission = True
                    self.lrpn = -1
                    if(self.list != []):
                        self.megaList.append(self.list)
                        self.list = []
                    self.packetCounter = 0
                    for x in self.megaList:
                        if(data in x[0]):
                            self.list = x
                            self.megaList.remove(self.list)
                if(not self.inTransmission):
                    continue
                if(packetNumber < self.lrpn):
                    packetNumber += 9
                for x in range(packetNumber - (self.lrpn + 1)):
                    self.list.append('')
                    self.packetCounter += 1
                if(len(self.list) > self.packetCounter):
                    self.list[self.packetCounter] = data
                else:
                    self.list.append(data)
                if(packetNumber != 0 and '|' in data):
                    if(self.verifyFile(self.list, self.packetCounter)):
                        string = ''.join(self.list)
                        fileData = string.split('|')
                        string = fileData[0] + '|' + fileData[1]
                        fileWithoutChecksum = string[:-2]
                        checksum = string[-2:]
                        if(self.checkChecksum(fileWithoutChecksum, checksum)):
                            fileData = fileWithoutChecksum.split('|')
                            f = open(fileData[0], 'w')
                            f.write(fileData[1])
                            f.close()
                            print('file has been written\n')
                            self.list = []
                            self.inTransmission = False
                        else:
                            print('checksum was not equal')
                self.lrpn = packetNumber
            finally:
                self.mutex.release()
            
receiver = DABreceiver("10.0.0.1", 4242)
t1 = Thread(target=receiver.main())
t1.start()

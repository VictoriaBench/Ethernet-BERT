import socket
from time import sleep, time
import config
from data_generator import DataGenerator, decodePacket
from bert import findErrors
from serial_reader import SerialReader
import math
import csv
import threading

class ReceiverSocket:
    def __init__(self) -> None:
        self.results = {}
        self.done = False
        self.receiver  = threading.Thread(target= self.receive)
        self.receiver.setDaemon(True)
        self.receiver.start()

    def stop(self):
        self.done = True

    def receive(self):
        with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(config.ETH_P_ALL)) as raw_socket:
            raw_socket.bind((config.INTERFACE, 0))
            expected_data_generator = DataGenerator(config.ETH_FRAME_LEN, config.NUM_PACKETS)
            serialReader = SerialReader('/dev/ttyACM0', 115200, 100)
            totalErrors = 0
            timer = time()
            while not self.done:
                data_raw = raw_socket.recv(config.ETH_FRAME_LEN)
                id, _ = decodePacket(data_raw)
                expected_data = expected_data_generator.getPacketFromID(id)      
                count, errors = findErrors(data_raw, expected_data)
                rxpower = serialReader.getJSONField("sfp0", "RXuW")
                if not rxpower: continue
                rxpowerDB = f"{10 * math.log(rxpower * 0.001,10):0.1f}"
                
                if rxpowerDB not in self.results.keys():
                    self.results[rxpowerDB] = [0,0]
                self.results[rxpowerDB][0] += errors
                self.results[rxpowerDB][1] += count
                totalErrors += errors 

        serialReader.stop()  

    def getResults(self):
        return self.results             
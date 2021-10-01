import socket
from time import sleep, time
import config
from data_generator import DataGenerator, decodePacket
from bert import findErrors
import traceback
from serial_reader import SerialReader
import math
import csv

results = {}

def receive():
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(config.ETH_P_ALL)) as raw_socket:
        with open("bertAtten.csv", 'w') as csv_file:
            raw_socket.bind((config.INTERFACE, 0))
            csv_writer = csv.writer(csv_file, delimiter=';')
            count = 0 
            expected_data_generator = DataGenerator(config.ETH_FRAME_LEN, config.NUM_PACKETS)
            serialReader = SerialReader('/dev/ttyACM0', 115200, 100)
            
            done = False
            totalErrors = 0
            while not done:
                try:
                    data_raw = raw_socket.recv(config.ETH_FRAME_LEN)
                    id, _ = decodePacket(data_raw)
                    expected_data = expected_data_generator.getPacketFromID(id)      
                    print(data_raw)
                    print(expected_data)
                    count, errors = findErrors(data_raw, expected_data)
                    rxpower = serialReader.getJSONField("sfp0", "RXuW")
                    rxpowerDB = f"({10 * math.log(rxpower * 0.001,10):0.1f}"
                    
                    if rxpowerDB not in results.keys():
                        results[rxpowerDB] = [0,0]
                    results[rxpowerDB][0] += errors
                    results[rxpowerDB][1] += count
                    totalErrors += errors
                except Exception:
                    print(traceback.format_exc())



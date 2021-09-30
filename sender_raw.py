import socket
from lt import encode
import time
from data_generator import DataGenerator
import config

with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(config.ETH_P_ALL)) as raw_socket:
    raw_socket.bind((config.INTERFACE, 0))   
    packetGenerator = DataGenerator(config.ETH_FRAME_LEN, config.NUM_PACKETS)
    print(f"Sending {config.NUM_PACKETS} packets ({config.NUM_PACKETS*config.ETH_FRAME_LEN/1024/1024}MB): ")
    start = time.perf_counter_ns()
    for packet in packetGenerator:
        raw_socket.sendall(packet)
    end = time.perf_counter_ns()
    print(f"\tcompleted in: {((end-start)/1000000):0.4f}ms")
    
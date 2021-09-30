from data_generator import DataGenerator, decodePacket
import time

dg = DataGenerator(22, 10)

for packet in dg:
    print(decodePacket(packet))
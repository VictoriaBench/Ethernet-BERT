from data_generator import DataGenerator, decodePacket
import time

dg = DataGenerator(17, 10, 5)

for packet in dg:
    print(decodePacket(packet))


print(decodePacket(dg.getPacketFromID(5)))
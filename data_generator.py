import random
import sys
import time
import io

class DataGenerator:
    def __init__(self, packetSize, numPackets, bufferSize = 100000, showTime = False) -> None:
        self.numPackets = numPackets
        self.packetSize = packetSize
        self.packetsGenerated = 0 
        self.showTime = showTime
        self.bufferSize = bufferSize
        self.buffer = io.BytesIO(b'')
        print("Generating buffer...")
        for i in range(self.bufferSize):
            self.buffer.write(self.generatePacketFromID(i))
        print("Done Generating")
   
    def __iter__(self):
        self.buffer.seek(0) 
        self.nextID = 0 
        return self

    def __next__(self):
        if self.numPackets is None or self.packetsGenerated <= self.numPackets:
            result = bytearray(self.buffer.read(self.packetSize))
            result[:12] = self.nextID.to_bytes(4, byteorder=sys.byteorder)*3
            self.nextID += 1
            self.packetsGenerated+=1
            if self.nextID >= self.bufferSize:
                self.buffer.seek((self.nextID % self.bufferSize) * self.packetSize)
            return result
        else:
            raise StopIteration


    def generatePacketFromID(self, id:int):
        if self.packetSize == 0:
            return b''
        if id >= self.bufferSize:
            return self.getPacketFromID(id)
        rand = random.Random(id)
        zero = 0
        header = zero.to_bytes(4, byteorder=sys.byteorder ) * 3
        integer = rand.getrandbits((self.packetSize - 12) * 8)
        result = header + integer.to_bytes(self.packetSize - 12, sys.byteorder)
        return result

    def getPacketFromID(self, id:int):
        prev = self.buffer.tell()
        val = (id % self.bufferSize) * self.packetSize
        self.buffer.seek(val)
        result = bytearray(self.buffer.read(self.packetSize))
        result[:12] = id.to_bytes(4, byteorder=sys.byteorder)*3
        self.buffer.seek(prev)
        return bytearray(result)

def decodePacket(data):
    ids = [int.from_bytes(data[:4], sys.byteorder), int.from_bytes(data[4:8], sys.byteorder), int.from_bytes(data[8:12], sys.byteorder)] 
    id = max(set(ids), key = ids.count)
    return id, data[12:]
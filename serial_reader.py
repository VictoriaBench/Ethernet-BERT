import serial
import re
from jupyterplot import ProgressPlot
import json
import math
import threading 
class SerialReader:
    def __init__(self, serialPort, baud, timeout):
        self.serialPort = serialPort
        self.baud = baud
        self.lock = threading.Lock()
        self.dataReader = threading.Thread(self.serialReader)
        self.dataReader.start()
        
    def getJSONField(self, field, subfield):
        with self.lock:
            if subfield: 
                return self.data[field][subfield]
            else:
                return self.data[field]

    def serialReader(self):
        with serial.Serial(self.serialPort, self.baud) as ser:
            ser.write(b"RAW\r\n")
            while True:
                ser_bytes = ser.readline() 
                try:    
                    with self.lock:
                        self.data =json.loads(ser_bytes)
                except:
                    continue
                # rxpower = sfpData["sfp0"]["RXuW"]
                # rxpowerDB = 10 * math.log(rxpower * 0.001,10)


   

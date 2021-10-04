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
        self.data = None
        self.done = False
        self.lock = threading.Lock()
        self.dataReader = threading.Thread(target=self.serialReader)
        self.dataReader.start()
        
    def getJSONField(self, field, subfield):
        with self.lock:
            if not self.data: return None
            if field not in self.data.keys(): return None
            return self.data[field][subfield]
         
    def stop(self):
        self.done = True
        
    def serialReader(self):
        with serial.Serial(self.serialPort, self.baud) as ser:
            print(f"Connected to serial port: {self.serialPort}")
            ser.write(b"RAW\r\n")
            while not self.done:
                ser_bytes = ser.readline() 
                with self.lock:
                    try:
                        self.data = json.loads(ser_bytes)
                    except: pass         
                # rxpower = sfpData["sfp0"]["RXuW"]
                # rxpowerDB = 10 * math.log(rxpower * 0.001,10)


   

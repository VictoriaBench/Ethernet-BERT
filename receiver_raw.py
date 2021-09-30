import socket
from time import sleep, time
import lt
import struct
import os
import random


ETH_P_ALL = 3
ETH_FRAME_LEN = 1514  # Max. octets in frame sans FCS
NUM_PACKETS =   100000
interface = 'enp1s0'

os.system(f'ethtool -K {interface} rx-all on')
os.system(f'ifconfig {interface} promisc')



with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL)) as raw_socket:
    raw_socket.bind((interface, 0))
    count = 0
    
    raw_socket.settimeout(1)
    timer = 0
    start = False
    received_ids = set()
    while True:
        try:
            data = raw_socket.recv(ETH_FRAME_LEN)
            id1 =  int.from_bytes(data[:4], "little")
            id2 =  int.from_bytes(data[4:8],"little")
            id3 =  int.from_bytes(data[8:12],"little")
            id4 =  int.from_bytes(data[12:16], "little")
        
            if start:
                if id1 == 0 or id1 in received_ids:
                    cont  = True
                if time() - timer > 6  or cont:
                    count = len(received_ids)
                    print(f"{count}/{NUM_PACKETS}  {count/NUM_PACKETS *100}%")
                    start = False
                    cont = False
                    continue
                
                received_ids.add(id1)

            if(id1 == 0 or id2 == 0 or id3 == 0 or id4 == 0) and not start:
                start = True
                print("starting")
                timer = time()
                received_ids = set()
                received_ids.add(0)         
        except:
            pass
          




            #error, count = BERT(data, expected_data)
            #total_count += count
            #total_error += error
        #header_data = data[:12]
        #header = struct.unpack('!III', header_data)
        #block_data = data[12:]
        #block = int.from_bytes(block_data, 'big')
        #decoder.consume_block((header,block))
        #if decoder.is_done():
        #    done = True

    #  with open('out.txt', 'wb') as f:
    #      decoder.stream_dump(f)
    #  print('\n')
    #  print(f"Total bits: {total_count}")
    #  print(f"Total errors: {total_error}")




import socket
from time import sleep, time
import config
from data_generator import DataGenerator, decodePacket
from bert import findErrors



with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(config.ETH_P_ALL)) as raw_socket:
    raw_socket.bind((config.INTERFACE, 0))
    count = 0 
    raw_socket.settimeout(1)
    timer = 0
    start = False
    received_ids = set()
    expected_data_generator = DataGenerator(config.ETH_FRAME_LEN, config.NUM_PACKETS)
    
    while True:
        try:
            data_raw = raw_socket.recv(config.ETH_FRAME_LEN)
            id, data = decodePacket(data_raw)
            expected_data = expected_data_generator.getPacketFromID(id)      
            count, errors = findErrors(data_raw, expected_data)
            print(errors, count)
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




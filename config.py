import os

ETH_P_ALL = 3
ETH_FRAME_LEN = 9216  # Max. octets in frame sans FCS
ETH_TYPE = 0x8015
BROADCAST_ADDR = b'\xFF\xFF\xFF\xFF\xFF\xFF'
NUM_PACKETS = 200000
INTERFACE = 'enp1s0'
MTU = 9216

os.system(f'ethtool -K {INTERFACE} rx-all on')
os.system(f'ifconfig {INTERFACE} promisc')
os.system(f'ip link set dev {INTERFACE} mtu {MTU}')
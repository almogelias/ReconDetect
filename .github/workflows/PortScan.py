from scapy.layers.inet import TCP,IP
from scapy.sendrecv import sr, sr1
import sys
from scapy import *


target = '192.168.222.2'
startport = 1200
endport = 1300
print("Scannig " +target+" for open TCP ports\n")

if startport==endport:
    endport+=1

for x in range(startport,endport):
    try:
        packet = IP(dst=target)/TCP(dport=x,flags='S')
        response = sr1(packet,timeout=0.01,verbose=0)
        if response.haslayer(TCP) and response.getlayer(TCP).flags==0x12:
            print('Port '+str(x)+' is open')
        sr(IP(dst=target)/TCP(dport=response.sport,flags='R'),timeout=0.01,verbose=0)
    except:
        continue
print('Scan is complite\n')
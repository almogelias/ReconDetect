from scapy.layers.inet import TCP, IP
from scapy.sendrecv import sr, sr1
import sys
from scapy import *



target = sys.argv[1]
startport = 1100
endport = startport+int(sys.argv[2])


print("\n \n")
print("     ###  Starting TCP PortScan {}    ###\n".format(target))
print("     ###  StartPort: {}   |   EndPort: {}    ###\n\n\n".format(startport,endport))

if startport == endport:
    endport += 1

for x in range(startport, endport):
    try:
        packet = IP(dst=target) / TCP(dport=x, flags='S')
        response = sr1(packet, timeout=0.1, verbose=0)
        if response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
            print('Scanning!!! Port number:' + str(x) + ' is open\n')
        else:
            print('Scanning!!! Port number:' + str(x) + ' is closed\n')
        sr(IP(dst=target) / TCP(dport=response.sport, flags='R'), timeout=0.01, verbose=0)
    except:
        continue
print("     \n###  End of flooding simulation  ###\n\n")

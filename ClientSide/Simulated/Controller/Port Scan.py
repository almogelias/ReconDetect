from scapy.layers.inet import TCP, IP
from scapy.sendrecv import sr, sr1
import sys
from scapy import *
from datetime import datetime
import os
import subprocess
from dbWriteSimulations import Database

target = sys.argv[1]
startport = 20
endport = startport+int(sys.argv[2])


def dbWriteAsncProcess(startTimePeriod, endTimePeriod, day):
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod, endTimePeriod, day)
    conn.updateFlows(startTimePeriod, endTimePeriod, day)
    conn.closeDbSession()


def timePeriodCalc():
    now = datetime.now()
    current_time = int(now.strftime("%H%M%S"))
    return '{}'.format(current_time - current_time % 10)


print("\n \n")
print("     ###  Starting TCP PortScan {}    ###\n".format(target))
print("     ###  StartPort: {}   |   EndPort: {}    ###\n\n\n".format(startport,endport))
day = datetime.today().strftime("%A")
startTimePeriod=timePeriodCalc()

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

endTimePeriod=str(int(timePeriodCalc())+10)

try:
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod,endTimePeriod,day)
    conn.updateFlows(startTimePeriod,endTimePeriod,day)
    conn.closeDbSession()
except Exception as e:
    print(e)
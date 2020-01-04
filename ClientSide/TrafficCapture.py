#####################################
'''
Main Program
'''
#####################################

from scapy.all import *
import psutil
from adapterInfo import Adapter
from parsePacket import Parser
#from PacketCounting import PacketCounting
#from Flow import Flow
from dbWrite import Database
import os
import datetime

### Global Variables ###
filter = "tcp"


### CallBack of Sniffer ###
def pkt_callback(pkt):
    # pkt.show() # debug statement - Full RawDATA
    # print(pkt.summary()) #debug Smaller RawDATA
    parser = Parser(pkt)
    conn.insertData(parser.dataDict)
    #packetsCount.addPacket(parser.dataDict)
    #flows.addPacket(parser.dataDict)
    parser.toStringPrint()
    createLogFile(writePath, fileNameWithTime, parser)
    ###Writing to file###


def createLogFile(writepath, fileNameWithTime, parser):
    # define the name of the file to be created
    mode = 'a' if os.path.exists(writepath) else 'w'
    with open(writepath + '\\' + fileNameWithTime, mode) as f:
        f.write(parser.toStringLog() + '\n')


### Create A Folder ###
def createFolder(writepath):
    # define the name of the directory to be created
    fileNameWithTime = fileName + '_' + str(
        int(datetime.datetime.now().timestamp())) + '.txt'  # Get File with Unix time
    try:
        os.mkdir(writepath)
    except OSError:

        my_file = os.path.join(writepath, fileNameWithTime)
        print("The directory {} already exist".format(writepath))
    else:
        print("Successfully created the directory {} ".format(writepath))
    return fileNameWithTime


### Find Online Network Adapter ###
def get_networkAdapter():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    available_networks = []
    for intface, addr_list in addresses.items():
        # if ("local area network" in intface.lower() or "wireless network connection" in intface.lower() or "Local Area Connection" in intface): #Search for Local Area Network name or Wireless adapter.
        # if ("local area network" in intface.lower() or "wireless network connection" in intface.lower() or "VMware Network Adapter VMnet8" in intface):  # Search for Local Area Network name or Wireless adapter.
        if intface in stats and getattr(stats[intface], "isup") and ('Loopback' not in intface):  # Get all the adapter which is up
            available_networks.append(
                Adapter(intface, addr_list[1].address, addr_list[1].netmask))  # Write Adapter info from adapterInfo.py
            print(addr_list[1].address)
        else:
            continue
    return (available_networks)


#### MAIN Func###
#packetsCount = PacketCounting()
#flows = Flow()
fileName = 'logfile'
writePath = 'C:\\Logs'
fileNameWithTime = createFolder(writePath)
conn=Database()
for onlineAdapter in get_networkAdapter():
    onlineAdapter.toString()
    print(onlineAdapter.ipNetworkWithPrefix())
    ### Calling Sniffer Driver (Scapy Lib)
    # sniff(iface=onlineAdapter.name, prn=pkt_callback, filter=filter +" "+"and src host {} and dst net {}".format(onlineAdapter.ip,onlineAdapter.ipNetworkWithPrefix()))
    sniff(iface=onlineAdapter.name, prn=pkt_callback, timeout=50,
              filter=filter + " " + "and src net {} and dst net {} and not host 192.168.222.254 and not dst host 192.168.222.255".format(
                  onlineAdapter.ipNetworkWithPrefix(), onlineAdapter.ipNetworkWithPrefix()))  # Sniff All !
    # sniff(iface=onlineAdapter.name, prn=pkt_callback, filter="tcp or icmp and src net {} and dst net {}".format(onlineAdapter.ipNetworkWithPrefix(),
    #        onlineAdapter.ipNetworkWithPrefix()), store=0, timeout=40)     #Capture filter TCP-Syn or ICMP and HostIP and dest=Network
#    print(packetsCount.table)
#    print (flows.flows)

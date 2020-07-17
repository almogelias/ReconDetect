#####################################

'''

Main Program

'''

#####################################



from scapy.all import *

import psutil

from adapterInfo import Adapter

from parsePacket import Parser

from PacketCounting import PacketCounting

from Flows import Flow
################
from PID import PID
################
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

    parser.toStringPrint()
    #########################################
    if flows.flows and flows.flows[0]['PID'] == parser.dataDict['PID']:
        # add to ProcessID queue
        pid.AddProcess(parser.dataDict)
    ##########################################

    packetsCount.addPacket(parser.dataDict, conn)

    flows.addPacket(parser.dataDict)

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

        if intface in stats and getattr(stats[intface], "isup") and ('Loopback' not in intface):  # Get all the adapter which is up

            available_networks.append(

                Adapter(intface, addr_list[1].address, addr_list[1].netmask))  # Write Adapter info from adapterInfo.py

            print(addr_list[1].address)

        else:

            continue

    return (available_networks)





#### MAIN Func###

packetsCount = PacketCounting()

flows = Flow()

pid = PID()

fileName = 'logfile'

writePath = 'C:\\temp'

fileNameWithTime = createFolder(writePath)

conn=Database()

for onlineAdapter in get_networkAdapter():

    onlineAdapter.toString()

    print(onlineAdapter.ipNetworkWithPrefix())

    ### Calling Sniffer Driver (Scapy Lib)
    while(True):
        d = datetime.datetime.now()
        if(d.hour in range(6, 23)):
            sniff(iface=onlineAdapter.name, prn=pkt_callback, timeout=30,

                      filter=filter + " " + "and src net {} and dst net {} and not host 192.168.222.254 and not host 192.168.222.255".format(

                          onlineAdapter.ipNetworkWithPrefix(), onlineAdapter.ipNetworkWithPrefix()))  # Sniff All !
            conn.insertPID(pid.Processes)
            conn.insertFlows(flows.flows)
            print(packetsCount.table)

            print (flows.flows)

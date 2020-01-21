#####################################
'''
Class of parsing packets fields.
'''
#####################################

import psutil
import socket
import os
from datetime import datetime
import tzlocal

class Parser():
    def __init__(self, pkt):
        self.pkt=pkt
        self.dataDict = self.parseData()

    def timePeriodCalc(self,time):
        return '{}'.format(time-time%10)
###Parsing Data - Main Method###
    def parseData(self): #Parse data with correct Protocol
        dataDict = {}
        dataDict=self.parseEthernet(dataDict)
        if self.pkt.payload._name=='ARP':
            return self.parseArpData(dataDict)
        elif self.pkt.payload._name=='IP':
            return self.parseIPData(dataDict)

#### Layer 2 Protocol
#### EtherNet ####

    def parseEthernet(self,dataDict):
        date = datetime.today()
        date_int=date.strftime("%d%m%Y")
        local_timezone = tzlocal.get_localzone()  # get pytz timezone
        local_time = datetime.fromtimestamp(self.pkt.time, local_timezone)
        dataDict["UnixTimeMillisec"] = int(self.pkt.time*1000)
        dataDict["Time"] = local_time.strftime('%H%M%S%f')
        dataDict["TimePeriod"] = self.timePeriodCalc(int(local_time.strftime('%H%M%S')))
        dataDict["Date"] = date_int
        dataDict["Day"] = local_time.strftime("%A")
        dataDict["srcMac"] = self.pkt.src
        dataDict["dstMac"] = self.pkt.dst
        dataDict["EthType"] = self.pkt.type
        return dataDict

### Layer 3 Protocol
###ARP###

    def parseArpData(self,dataDict):
        dataDict["Protocol"]=self.pkt.payload._name
        dataDict["srcIpAddr"] = self.pkt.payload.psrc
        dataDict["dstIpAddr"] = self.pkt.payload.pdst
        dataDict["Hwtype"] = self.pkt.payload.hwtype
        dataDict["Ptype"] = self.pkt.payload.ptype
        dataDict["Hwlen"] = self.pkt.payload.hwlen
        dataDict["Plen"] = self.pkt.payload.plen
        dataDict["Op"] = self.pkt.payload.op
        return dataDict

###IP###
    def parseIPData(self,dataDict):
        #dataDict["Protocol"] = self.pkt.payload._name
        dataDict["srcIpAddr"] = self.pkt.payload.src
        dataDict["dstIpAddr"] = self.pkt.payload.dst
        #dataDict["IPver"] = self.pkt.payload.version
        #dataDict["Ihl"] = self.pkt.payload.ihl
        #dataDict["Tos"] = self.pkt.payload.tos
        dataDict["IPLen"] = self.pkt.payload.len
        dataDict["ID"] = self.pkt.payload.id
        #dataDict["Frag"] = self.pkt.payload.frag
        dataDict["Ttl"] = self.pkt.payload.ttl
        dataDict["Proto"] = self.pkt.payload.proto
        dataDict["IPChksum"] = self.pkt.payload.chksum

###Call TCP / UDP Parsing

        if(self.pkt.payload.payload._name=='TCP'):
            return self.parseTCPData(dataDict)
        elif(self.pkt.payload.payload._name=='UDP'):
            return self.parseUDPData(dataDict)
        elif self.pkt.payload.payload._name=='ICMP':
            return self.parseIcmpData(dataDict)
        return dataDict

    def parseIcmpData(self,dataDict):
        dataDict["ipProtocol"] = self.pkt.payload.payload._name
        dataDict["IcmpType"] = self.pkt.payload.payload.type
        dataDict["IcmpCode"] = self.pkt.payload.payload.code
        dataDict["IcmpChksum"] = self.pkt.payload.payload.chksum
        dataDict["IcmpId"] = self.pkt.payload.payload.id
        dataDict["IcmpTsOri"] = self.pkt.payload.payload.ts_ori
        dataDict["IcmpTsRx"] = self.pkt.payload.payload.ts_rx
        dataDict["IcmpTsTx"] = self.pkt.payload.payload.ts_tx
        dataDict["IcmpGw"] = self.pkt.payload.payload.gw
        dataDict["IcmpPtr"] = self.pkt.payload.payload.ptr
        dataDict["IcmpReserved"] = self.pkt.payload.payload.reserved
        dataDict["IcmpLength"] = self.pkt.payload.payload.length
        dataDict["IcmpAddrMask"] = self.pkt.payload.payload.addr_mask
        dataDict["IcmpNextHopMtu"] = self.pkt.payload.payload.nexthopmtu
        dataDict["IcmpUnused"] = self.pkt.payload.payload.unused
        return dataDict


#### Layer 4 - TCP

    def parseTCPData(self,dataDict):
        dataDict["ipProtocol"] = self.pkt.payload.payload._name
        dataDict["srcPort"] = self.pkt.payload.payload.sport
        dataDict["dstPort"] = self.pkt.payload.payload.dport
        dataDict["service"] = self.get_service(dataDict["dstPort"],dataDict["srcPort"])
        dataDict["Seq"] = self.pkt.payload.payload.seq
        dataDict["Ack"] = self.pkt.payload.payload.ack
        dataDict["dataOfs"] = self.pkt.payload.payload.dataofs
        #dataDict["Reserved"] = self.pkt.payload.payload.reserved
        dataDict["Flags"] = str(self.pkt.payload.payload.flags)
        dataDict["Window"] = self.pkt.payload.payload.window
        dataDict["TcpChksum"] = self.pkt.payload.payload.chksum
        #dataDict["Urgptr"] = self.pkt.payload.payload.urgptr
        #dataDict["Options"] = self.pkt.payload.payload.options


### Get PID + FileName.exe/dll
        pid = self.getPID()
        dataDict["PID"] = str(pid)
        if(dataDict["PID"]!='None'):
            (fileName, filePath) = self.getFileNamePerPID(pid)
            deltaTime = self.getFileDeltaTime(filePath)
            if (fileName != "None" and deltaTime!="None"):
                dataDict["fileName"] = fileName
                dataDict["filePath"] = filePath
                dataDict["deltaTimeMillisec"] = int(deltaTime*1000)
        return dataDict


### Layer 4 - UDP
    def parseUDPData(self, dataDict):
        dataDict["ipProtocol"] = self.pkt.payload.payload._name
        dataDict["srcPort"] = self.pkt.payload.payload.sport
        dataDict["dstPort"] = self.pkt.payload.payload.dport
        dataDict["UdpLen"] = self.pkt.payload.payload.len
        dataDict["UdpChksum"] = self.pkt.payload.payload.chksum


        ### Get PID + FileName.exe/dll
        pid = self.getPID()
        dataDict["PID"] = str(pid)
        if (dataDict["PID"] != 'None'):
            (fileName, filePath) = self.getFileNamePerPID(pid)
            deltaTime = self.getFileDeltaTime(filePath)
            if (fileName != "None"):
                dataDict["fileName"] = fileName
                dataDict["filePath"] = filePath
                dataDict["deltaTime"] = deltaTime
        return dataDict

    ### Get service for known port number
    def get_service(self,dstport,srcport):
        try:
            if(dstport<1023):
                service = socket.getservbyport(dstport).lower()
            else:
                service = socket.getservbyport(srcport).lower()
            return service
        except:
            return 'None'


    #### Get PID Per Connection - Searching for PID ####

    def getPID(self):
        connections = psutil.net_connections()
        for sconn in connections:
            if(sconn.status!='NONE' and sconn.status!='LISTEN' and sconn.status!='CLOSE_WAIT' and (sconn.raddr!=())):
                #print(sconn)  # Check Process connection.
                if (sconn.laddr.ip == self.pkt.payload.src) and (sconn.raddr.ip == self.pkt.payload.dst) and (sconn.raddr.port == self.pkt.payload.payload.dport):
                    return(sconn.pid)

#### GET Proccess Name Per PID ####
    def getFileNamePerPID(self,PID):
        try:
            if(PID!=0 and PID!=4):
                file = psutil.Process(PID)
                filename = file.name()
                filepath = file.exe()
                return (filename,filepath)
            elif (PID==4):
                return ('System','None')
            else:
                return('System Idle Process.exe','None')
        except:
            return ('None','None')

    def getFileDeltaTime(self,filePath):
        if(filePath!='None'):
            creationTime = os.path.getctime(filePath)
            deltaTime=self.pkt.time-creationTime
            return deltaTime
        return 'None'

###Printing Data####
    def toStringPrint(self):
        print (self.dataDict)


###Returning DataLOG###

    def toStringLog(self):
        return str(self.dataDict)

'''
###Returning DataLOG###

    def toStringLog(self):
        return(str(self.dataDict["unixTime"]) + ',' + self.dataDict["srcMac"] + ',' + self.dataDict["dstMac"] +  # Ethernet
              ',' + self.dataDict["srcIpAddr"] + ',' + self.dataDict["dstIpAddr"] +  # IP
              ',' + self.dataDict["protocol"] + ',' + str(self.dataDict["dstPort"]) + ',' + str(self.dataDict["tcpFlag"]))  # Protocol
'''


'''

###Printing Data####

    def toStringPrint(self):
        print(str(self.dataDict["unixTime"]) + ',   ' + self.dataDict["srcMac"] + ',    ' + self.dataDict["dstMac"]+ # Ethernet
              ',    ' + self.dataDict["srcIpAddr"] +',  ' + self.dataDict["dstIpAddr"]+                              # IP
              ',   '+ self.dataDict["protocol"]+',  '+str(self.dataDict["dstPort"])+',  '+str(self.dataDict["tcpFlag"]))                                      #Protocol

'''

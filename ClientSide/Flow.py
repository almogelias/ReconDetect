import json
from heapq import heapify, heappush, heappop
from collections import deque

class Flow:
    maxSize = 2500

    def __init__(self):
        self.count = 0
        self.flows = deque()
        self.paCount = 0


    def addPacket(self,packet):
        dictPacketSummery={'Time':packet['Time'],
                           'srcIpAddr':packet['srcIpAddr'],
                           'dstIpAddr':packet['dstIpAddr'],
                           'ipProtocol':packet['ipProtocol'],
                           'dstPort':packet['dstPort'],
                           'counterOfPackets':0,
                           'counterOfPa':0
                           }
        if (self.count==0):
            self.count = self.count + 1
            dictPacketSummery['counterOfPackets'] += 1
            self.flows.appendleft(dictPacketSummery)
        else:
            try:
                if(packet['Flags']=='S' and packet['Ack']==0):
                    dictPacketSummery['counterOfPackets'] += 1
                    self.flows.appendleft(dictPacketSummery)
                    self.count = self.count + 1
                else:
                    ##Not new and Not Syn - Add to Old Flow
                    for flow in self.flows:
                        if (flow['dstPort'] == packet['dstPort'] or flow['dstPort']==packet['srcPort']):
                            flow['counterOfPackets']+=1
                            if(packet['Flags']=='PA'):
                                flow['counterOfPa'] +=1
                    if(packet['Flags']=='FA'):
                        for flow in self.flows:
                            if ((flow['dstPort'] == packet['dstPort'] or flow['dstPort']==packet['srcPort']) and (flow['srcIpAddr']==packet['srcIpAddr'])):
                                flow['counterOfPackets'] += 1
                                print('------------------------')
                                print(flow)
            except:
                pass


    def FlowsToString(self):
        for flows in self.flow:
            print (flows)

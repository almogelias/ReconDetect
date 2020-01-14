from collections import deque


class Flow:

    def __init__(self):

        self.flows = deque()

    def addCounterToDictFlow(self, packet, dictFlowSummery):
        if (packet['Flags'] == 'S'):
            dictFlowSummery['counterOfSyn'] += 1
        if (packet['Flags'] == 'A'):
            dictFlowSummery['counterOfAck'] += 1
        if (packet['Flags'] == 'PA'):
            dictFlowSummery['counterOfPa'] += 1
        if (packet['Flags'] == 'R'):
            dictFlowSummery['counterOfR'] += 1
        if (packet['Flags'] == 'RA'):
            dictFlowSummery['counterOfRA'] += 1
        if (packet['Flags'] == 'FA'):
            dictFlowSummery['counterOfFin'] += 1
        dictFlowSummery['counterOfPackets'] += 1
        dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
        dictFlowSummery['packetsTotalSize'] = packet['IPLen']
        return dictFlowSummery

    def addCounterInExistFlow(self, flow, packet, dictFlowSummery):
        flow['counterOfPackets'] += 1
        if (packet['Flags'] == 'S'):
            flow['counterOfSyn'] += 1
        if (packet['Flags'] == 'A'):
            flow['counterOfAck'] += 1
        if (packet['Flags'] == 'PA'):
            flow['counterOfPa'] += 1
        if (packet['Flags'] == 'R'):
            flow['counterOfR'] += 1
        if (packet['Flags'] == 'RA'):
            flow['counterOfRA'] += 1
        if (packet['Flags'] == 'FA'):
            flow['counterOfFin'] += 1
        flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
        flow['packetsTotalSize'] += packet['IPLen']
        return flow

    def reset_dictFlowSummery(self,packet):
        dictFlowSummery = {'UnixStartTimeMillisec': packet['UnixTimeMillisec'],
                           'UnixEndTimeMillisec': 0,
                           'Time': packet['Time'],
                           'Day': packet['Day'],
                           'srcIpAddr': packet['srcIpAddr'],
                           'dstIpAddr': packet['dstIpAddr'],
                           'Service': packet['service'],
                           'srcPort': packet['srcPort'],
                           'dstPort': packet['dstPort'],
                           'counterOfPackets': 0,
                           'counterOfSyn': 0,
                           'counterOfAck': 0,
                           'counterOfPa': 0,
                           'counterOfR': 0,
                           'counterOfRA': 0,
                           'counterOfFin': 0,
                           'packetsTotalSize': 0
                           }
        return dictFlowSummery

    def addPacket(self, packet):

        if ((packet['dstPort'] != 445 and packet['srcPort'] != 445) and
                (packet['dstPort'] != 1433 and packet['srcPort'] != 1433)):

            dictFlowSummery=self.reset_dictFlowSummery(packet)
            checkIfFlowExist=0
            index=0
            for flow in self.flows:

                if (((flow['dstPort'] == packet['dstPort'] and flow['srcPort'] == packet['srcPort'] and (flow['srcIpAddr'] == packet['srcIpAddr'])) or (
                        flow['dstPort'] == packet['srcPort'] and flow['srcPort'] == packet['dstPort']) and (flow['srcIpAddr'] == packet['dstIpAddr']))):
                    self.flows[index]=self.addCounterInExistFlow(flow, packet, dictFlowSummery)
                    checkIfFlowExist=1
                index += 1

            if (checkIfFlowExist==0):
                dictFlowSummery=self.addCounterToDictFlow(packet,dictFlowSummery)
                self.flows.appendleft(dictFlowSummery)


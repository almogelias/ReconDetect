from collections import deque


class Flow:

    def __init__(self):

        self.flowCount = 0

        self.flows = deque()

    def addPacket(self, packet):

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
                           'packetsTotalSize': 0,
                           ################################
                           'PID':None
                           ################################
                           }

        try:

            if ((packet['dstPort'] != 445 and packet['srcPort'] != 445) and (packet['dstPort'] != 1433 and packet['srcPort'] != 1433)):

                if self.flows:

                    for flow in self.flows:

                        if (((flow['dstPort'] == packet['dstPort'] and flow['srcPort'] == packet['srcPort'] and (flow['srcIpAddr'] == packet['srcIpAddr']) and (flow['dstIpAddr'] == packet['dstIpAddr'])) or
                             (flow['dstPort'] == packet['srcPort'] and flow['srcPort'] == packet['dstPort'] and (flow['srcIpAddr'] == packet['dstIpAddr']) and (flow['dstIpAddr'] == packet['dstIsrcIpAddrpAddr'])))
                                 and flow['counterOfFin'] == 0):
                            flow['counterOfPackets'] += 1
                            flow['packetsTotalSize'] += packet['IPLen']
                            flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                            if(packet['Flags']=='S'):
                                flow['counterOfSyn'] += 1
                            elif (packet['Flags'] == 'A'):
                                flow['counterOfAck'] += 1
                            elif (packet['Flags'] == 'PA'):
                                flow['counterOfPa'] += 1
                            elif (packet['Flags'] == 'R'):
                                flow['counterOfR'] += 1
                            elif (packet['Flags'] == 'RA'):
                                flow['counterOfRA'] += 1
                            elif (packet['Flags'] == 'FA'):
                                flow['counterOfFin'] += 1

                        else:
                            dictFlowSummery['counterOfPackets'] += 1
                            dictFlowSummery['packetsTotalSize'] += packet['IPLen']
                            dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                            if (packet['Flags'] == 'S'):
                                dictFlowSummery['counterOfSyn'] += 1
                            elif (packet['Flags'] == 'A'):
                                dictFlowSummery['counterOfAck'] += 1
                            elif (packet['Flags'] == 'PA'):
                                dictFlowSummery['counterOfPa'] += 1
                            elif (packet['Flags'] == 'R'):
                                dictFlowSummery['counterOfR'] += 1
                            elif (packet['Flags'] == 'RA'):
                                dictFlowSummery['counterOfRA'] += 1
                            elif (packet['Flags'] == 'FA'):
                                dictFlowSummery['counterOfFin'] += 1
                            self.flows.appendleft(dictFlowSummery)
                else:
                    dictFlowSummery['counterOfPackets'] += 1
                    dictFlowSummery['packetsTotalSize'] += packet['IPLen']
                    dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                    if (packet['Flags'] == 'S'):
                        dictFlowSummery['counterOfSyn'] += 1
                    elif (packet['Flags'] == 'A'):
                        dictFlowSummery['counterOfAck'] += 1
                    elif (packet['Flags'] == 'PA'):
                        dictFlowSummery['counterOfPa'] += 1
                    elif (packet['Flags'] == 'R'):
                        dictFlowSummery['counterOfR'] += 1
                    elif (packet['Flags'] == 'RA'):
                        dictFlowSummery['counterOfRA'] += 1
                    elif (packet['Flags'] == 'FA'):
                        dictFlowSummery['counterOfFin'] += 1
                    ##############################
                    if(packet['PID']):
                        dictFlowSummery['PID']=packet['PID']
                    ##############################
                    self.flows.appendleft(dictFlowSummery)



        except:

            pass

    def returnFlows(self):

        for flow in self.flows:
            print(flow)

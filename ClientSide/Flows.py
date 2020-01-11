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
                           'packetsTotalSize': 0
                           }

        try:

            if ((packet['dstPort'] != 445 and packet['srcPort'] != 445) and (packet['dstPort'] != 1433 and packet['srcPort'] != 1433)):

                if (packet['Flags'] == 'S' and packet['Ack'] == 0):

                    ####there are no flows - INIT

                    AlreadyWasSynInFlow = 0

                    for flow in self.flows:

                        if (((flow['dstPort'] == packet['dstPort'] and flow['srcPort'] == packet['srcPort']) or (
                                flow['dstPort'] == packet['srcPort'] and flow['srcPort'] == packet['dstPort']))
                                and (flow['srcIpAddr'] == packet['srcIpAddr'])):
                            AlreadyWasSynInFlow = 1
                            flow['counterOfPackets'] += 1
                            flow['counterOfSyn'] += 1
                            flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                            flow['packetsTotalSize'] += packet['IPLen']

                    if (AlreadyWasSynInFlow == 0):
                        dictFlowSummery['counterOfSyn'] += 1
                        dictFlowSummery['counterOfPackets'] += 1
                        dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                        dictFlowSummery['packetsTotalSize'] = packet['IPLen']
                        self.flows.appendleft(dictFlowSummery)

                else:

                    #if (self.flows()):
                    ####Flows not empty####

                    if (packet['Flags'] == 'FA'):

                        if self.flows:

                            for flow in self.flows:

                                if (((flow['dstPort'] == packet['dstPort'] and flow['srcPort'] == packet[
                                    'srcPort']) or (flow['dstPort'] == packet['srcPort'] and flow['srcPort'] == packet[
                                    'dstPort']))
                                        and (flow['srcIpAddr'] == packet['srcIpAddr']) and flow['counterOfFin'] == 0):

                                    flow['counterOfFin'] = 1
                                    flow['counterOfPackets'] = flow['counterOfPackets'] + 1
                                    flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                    flow['packetsTotalSize'] += packet['IPLen']
                                    dictFlowSummery[
                                        'UnixEndTimeMillisec', 'counterOfPackets', 'counterOfSyn', 'counterOfAck', 'counterOfPa','packetsTotalSize'] = 0

                        else:

                            dictFlowSummery['counterOfFin'] += 1
                            dictFlowSummery['counterOfPackets'] += 1
                            dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                            dictFlowSummery['packetsTotalSize'] = packet['IPLen']
                            self.flows.appendleft(dictFlowSummery)



                    elif (packet['Flags'] == 'A'):

                        if self.flows:

                            for flow in self.flows:

                                if (((flow['dstPort'] == packet['dstPort'] and flow['srcPort'] == packet[
                                    'srcPort']) or (flow['dstPort'] == packet['srcPort'] and flow['srcPort'] == packet[
                                    'dstPort']))

                                        and (flow['srcIpAddr'] == packet['srcIpAddr'])):
                                    flow['counterOfAck'] = 1
                                    flow['counterOfPackets'] = flow['counterOfPackets'] + 1
                                    flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                    flow['packetsTotalSize'] += packet['IPLen']
                                    dictFlowSummery[
                                        'UnixEndTimeMillisec', 'counterOfPackets', 'counterOfSyn', 'counterOfAck', 'counterOfPa','packetsTotalSize'] = 0

                        else:

                            dictFlowSummery['counterOfAck'] += 1
                            dictFlowSummery['counterOfPackets'] += 1
                            dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                            dictFlowSummery['packetsTotalSize'] = packet['IPLen']
                            self.flows.appendleft(dictFlowSummery)

                    ##Not new and Not Syn - Add to old Flow

                    if self.flows:

                        for flow in self.flows:

                            if (packet['Flags'] != 'SA'):

                                if (((flow['dstPort'] == packet['dstPort'] and flow['srcPort'] == packet['srcPort']) or (
                                        flow['dstPort'] == packet['srcPort'] and flow['srcPort'] == packet['dstPort'])) and
                                        flow['counterOfFin'] == 0):

                                    if (packet['Flags'] == 'PA'):

                                        flow['counterOfPa'] = flow['counterOfPa'] + 1
                                        flow['counterOfPackets'] = flow['counterOfPackets'] + 1
                                        flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                        flow['packetsTotalSize'] += packet['IPLen']

                                    elif (packet['Flags'] == 'A'):

                                        flow['counterOfAck'] = flow['counterOfAck'] + 1
                                        flow['counterOfPackets'] = flow['counterOfPackets'] + 1
                                        flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                        flow['packetsTotalSize'] += packet['IPLen']

                                    elif (packet['Flags'] == 'R'):

                                        flow['counterOfR'] += 1
                                        flow['counterOfPackets'] += 1
                                        flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                        flow['packetsTotalSize'] += packet['IPLen']

                                    elif (packet['Flags'] == 'RA'):

                                        flow['counterOfRA'] += 1
                                        flow['counterOfPackets'] += 1
                                        flow['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                        flow['packetsTotalSize'] += packet['IPLen']

                    else:

                                if (packet['Flags'] == 'PA'):

                                    dictFlowSummery['counterOfPa'] += 1
                                    dictFlowSummery['counterOfPackets'] += 1
                                    dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                    dictFlowSummery['packetsTotalSize'] = packet['IPLen']
                                    self.flows.appendleft(dictFlowSummery)

                                elif (packet['Flags'] == 'R'):

                                    dictFlowSummery['counterOfR'] += 1
                                    dictFlowSummery['counterOfPackets'] += 1
                                    dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                    dictFlowSummery['packetsTotalSize'] = packet['IPLen']
                                    self.flows.appendleft(dictFlowSummery)

                                elif (packet['Flags'] == 'RA'):

                                    dictFlowSummery['counterOfRA'] += 1
                                    dictFlowSummery['counterOfPackets'] += 1
                                    dictFlowSummery['UnixEndTimeMillisec'] = packet['UnixTimeMillisec']
                                    dictFlowSummery['packetsTotalSize'] = packet['IPLen']
                                    self.flows.appendleft(dictFlowSummery)


        except:

            pass

    def returnFlows(self):

        for flow in self.flows:
            print(flow)

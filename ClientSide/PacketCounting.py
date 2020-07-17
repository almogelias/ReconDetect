from collections import deque


class PacketCounting:

    def __init__(self):
        self.TenSeconds = 0
        self.table = deque()

    def addPacket(self, packet,conn):
        if not (packet['dstPort'] == 1433 or packet['srcPort'] == 1433):
            packets = {
                'TimePeriod': 0,
                'startTimeUnixMillisec': 0,
                'endTimeUnixMillisec': 0,
                'TenSeconds': self.TenSeconds,
                'Day': '',
                'packetCount': 0,
                'counterOfSyn': 0,
                'counterOfAck': 0,
                'counterOfPa': 0,
                'counterOfR':0,
                'counterOfRA':0,
                'counterOfFin': 0,
                'packetsTotalSize':0
            }



            if self.table:
                ####There is value###
                if (self.table[0]["TimePeriod"] == packet["TimePeriod"] and self.table[0]["Day"] == packet["Day"]):
                    self.table[0]["endTimeUnixMillisec"] = packet["UnixTimeMillisec"]
                    self.table[0]["packetCount"] += 1
                    if (packet['Flags'] == 'S'):
                        self.table[0]['counterOfSyn'] += 1
                    if (packet['Flags'] == 'A'):
                        self.table[0]['counterOfAck'] += 1
                    if (packet['Flags'] == 'PA'):
                        self.table[0]['counterOfPa'] += 1
                    if (packet['Flags'] == 'R'):
                        self.table[0]['counterOfR'] += 1
                    if (packet['Flags'] == 'RA'):
                        self.table[0]['counterOfRA'] += 1
                    if (packet['Flags'] == 'FA'):
                        self.table[0]['counterOfFin'] += 1
                    self.table[0]["packetsTotalSize"]+=packet["IPLen"]



                else:

                    ##################
                    ##  Write to DB ##
                    ##################
                    conn.insertCountsTenSecond(self.table[0])

                    ##################
                    ##  New Count   ##
                    ##################
                    try:
                        packets["startTimeUnixMillisec"] = packet["UnixTimeMillisec"]
                        # packets["endTimeUnixMillisec"] = packet["UnixTimeMillisec"]
                        self.TenSeconds += 1
                        packets["TenSeconds"] = self.TenSeconds
                        packets["TimePeriod"] = packet['TimePeriod']
                        packets["Day"] = packet["Day"]
                        packets['packetCount'] += 1
                        if (packet['Flags'] == 'S'):
                            packets['counterOfSyn'] += 1
                        if (packet['Flags'] == 'A'):
                            packets['counterOfAck'] += 1
                        if (packet['Flags'] == 'PA'):
                            packets['counterOfPa'] += 1
                        if (packet['Flags'] == 'R'):
                            packets['counterOfReset'] += 1
                        if (packet['Flags'] == 'RA'):
                            packets['counterOfResetAck'] += 1
                        if (packet['Flags'] == 'FA'):
                            packets['counterOfFin'] += 1
                        packets["packetsTotalSize"]= packet["IPLen"]
                        self.table.appendleft(packets)
                    except:
                        try:
                            print ('Trying again !!!')
                            packets["startTimeUnixMillisec"] = packet["UnixTimeMillisec"]
                            # packets["endTimeUnixMillisec"] = packet["UnixTimeMillisec"]
                            self.TenSeconds += 1
                            packets["TenSeconds"] = self.TenSeconds
                            packets["TimePeriod"] = packet['TimePeriod']
                            packets["Day"] = packet["Day"]
                            packets['packetCount'] += 1
                            if (packet['Flags'] == 'S'):
                                packets['counterOfSyn'] += 1
                            if (packet['Flags'] == 'A'):
                                packets['counterOfAck'] += 1
                            if (packet['Flags'] == 'PA'):
                                packets['counterOfPa'] += 1
                            if (packet['Flags'] == 'R'):
                                packets['counterOfReset'] += 1
                            if (packet['Flags'] == 'RA'):
                                packets['counterOfResetAck'] += 1
                            if (packet['Flags'] == 'FA'):
                                packets['counterOfFin'] += 1
                            packets["packetsTotalSize"] = packet["IPLen"]
                            self.table.appendleft(packets)
                        except:
                            print('Packet loss!!!')
            else:



                #### the table is empty ###
                packets["startTimeUnixMillisec"] = packets["endTimeUnixMillisec"] = packet["UnixTimeMillisec"]
                self.TenSeconds += 1
                packets["TenSeconds"] = self.TenSeconds
                packets["TimePeriod"] = packet['TimePeriod']
                packets["Day"] = packet["Day"]
                packets['packetCount'] += 1
                if (packet['Flags'] == 'S'):
                    packets['counterOfSyn'] += 1
                if (packet['Flags'] == 'A'):
                    packets['counterOfAck'] += 1
                if (packet['Flags'] == 'PA'):
                    packets['counterOfPa'] += 1
                if (packet['Flags'] == 'R'):
                    packets['counterOfReset'] += 1
                if (packet['Flags'] == 'RA'):
                    packets['counterOfResetAck'] += 1
                if (packet['Flags'] == 'FA'):
                    packets['counterOfFin'] += 1
                packets['packetsTotalSize'] = packet["IPLen"]
                self.table.appendleft(packets)
            return self.table


    def returnTable(self):
        for row in self.table:
            print(row)

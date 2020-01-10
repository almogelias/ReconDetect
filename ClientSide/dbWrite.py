import pyodbc

Driver = 'ODBC Driver 17 for SQL Server'
Server = 'LabSRV'
DB = 'FinalProject'


def connectSQLServer(driver, server, db):
    connSQLServer = pyodbc.connect(
        r'DRIVER={' + driver + '};'
                               r'SERVER=' + server + ';'
                                                     r'DATABASE=' + db + ';'
                                                                         r'UID=sa;'
                                                                         r'PWD=Ll123456'

    )
    return connSQLServer


class Database():
    def __init__(self):
        self.conn = connectSQLServer(Driver, Server, DB)

    def insertFlows(self, flows):
        curs = self.conn.cursor()
        for flow in flows:
            try:
                query="""SELECT FlowID FROM [FinalProject].[dbo].[Flows] 
                            Where ((srcIpAddr = '{}' and dstIpAddr='{}'
                            and Service='{}' and srcPort='{}' and dstPort='{}')
                            or
                            (srcIpAddr = '{}' and dstIpAddr='{}'
                            and Service='{}' and srcPort='{}' and dstPort='{}'))
                            and
                            counterOfFin=0
                            and
                            (({}-UnixEndTimeMillisec)/(1000))<120;""".format(
                    flow["srcIpAddr"],
                    flow["dstIpAddr"],
                    flow["Service"],
                    flow["srcPort"],
                    flow["dstPort"],
                    flow["srcIpAddr"],
                    flow["dstIpAddr"],
                    flow["Service"],
                    flow["srcPort"],
                    flow["dstPort"],
                    flow['UnixStartTimeMillisec']
                )
                results = curs.execute(query)
                print (results)
            except:
                query = """INSERT INTO  dbo.Flows values({},{},{},'{}','{}','{}','{}',{},{},{},{},{},{},{},{})""".format(
                    flow["UnixStartTimeMillisec"],
                    flow["UnixEndTimeMillisec"],
                    flow["Time"],
                    flow["Day"],
                    flow["srcIpAddr"],
                    flow["dstIpAddr"],
                    flow["Service"],
                    flow["srcPort"],
                    flow["dstPort"],
                    flow["counterOfPackets"],
                    flow["counterOfSyn"],
                    flow["counterOfPa"],
                    flow["counterOfR"],
                    flow["counterOfRA"],
                    flow["counterOfFin"]
                )
                curs.execute(query)
                curs.commit()

    def insertCountsTenSecond(self, lastPacketCounting):
        curs = self.conn.cursor()
        try:
            query = """UPDATE dbo.packetsCountTenSecond
             SET endTimeUnixMillisec={}
             packetCount={}
             counterOfSyn={}
             counterOfAck={}
             counterOfPa={}
             counterOfR={}
             counterOfRA={}
             counterOfFin={}
             WHERE TimePeriod={}""".format(lastPacketCounting["endTimeUnixMillisec"], lastPacketCounting["packetCount"],
                                           lastPacketCounting["counterOfSyn"],
                                           lastPacketCounting["counterOfAck"],
                                           lastPacketCounting["counterOfPa"],
                                           lastPacketCounting["counterOfR"],
                                           lastPacketCounting["counterOfRA"],
                                           lastPacketCounting["counterOfFin"],
                                           lastPacketCounting["TimePeriod"])
            curs.execute(query)
            curs.commit()

        except:
            query = """INSERT INTO  dbo.packetsCountTenSecond values({},{},{},'{}',{},{},{},{},{},{},{})""".format(
                lastPacketCounting["TimePeriod"],
                lastPacketCounting["startTimeUnixMillisec"],
                lastPacketCounting["endTimeUnixMillisec"],
                lastPacketCounting["Day"],
                lastPacketCounting["packetCount"],
                lastPacketCounting["counterOfSyn"],
                lastPacketCounting["counterOfAck"],
                lastPacketCounting["counterOfPa"],
                lastPacketCounting["counterOfR"],
                lastPacketCounting["counterOfRA"],
                lastPacketCounting["counterOfFin"]
            )
            curs.execute(query)
            curs.commit()

    def insertData(self, dataDict):
        curs = self.conn.cursor()
        try:
            self.insertCountsTenSecond(dataDict, curs)

        except Exception as e:
            print(e)
            curs.rollback()

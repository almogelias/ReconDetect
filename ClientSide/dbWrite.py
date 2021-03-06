import pyodbc



Driver = 'ODBC Driver 17 for SQL Server'
Server = 'DESKTOP-GRTRD9G'
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

        if flows:

            for flow in flows:

                ### check if exist less than 180

                query = """SELECT FlowID,UnixStartTimeMillisec,counterOfPackets,counterOfSyn,counterOfPa,counterOfR,counterOfRA,counterOfFin,packetsTotalSize

                            FROM [FinalProject].[dbo].[Flows] 

                            Where ((srcIpAddr = '{}' and dstIpAddr='{}'

                            and Service='{}' and srcPort='{}' and dstPort='{}')

                            or

                            (srcIpAddr = '{}' and dstIpAddr='{}'

                            and Service='{}' and srcPort='{}' and dstPort='{}'))

                            and

                            (({}-UnixStartTimeMillisec)/(1000))<180;""".format(



                    flow["srcIpAddr"],

                    flow["dstIpAddr"],

                    flow["Service"],

                    flow["srcPort"],

                    flow["dstPort"],

                    flow["dstIpAddr"],

                    flow["srcIpAddr"],

                    flow["Service"],

                    flow["dstPort"],

                    flow["srcPort"],

                    flow['UnixStartTimeMillisec']

                )

                curs.execute(query)

                result = {}

                for row in curs:

                    result = row

                if result:
                    #### there is Flow in the DB ###

                    newCounterOfPackets = flow['counterOfPackets'] + row[2]

                    newCounterOfSyn = flow['counterOfSyn'] + row[3]

                    newCounterOfPa = flow['counterOfPa'] + row[4]

                    newCounterOfR = flow['counterOfR'] + row[5]

                    newCounterOfRA = flow['counterOfRA'] + row[6]

                    newCounterOfFin = flow['counterOfFin'] + row[7]

                    newSumOfFlowSize = flow['packetsTotalSize'] + row[8]

                    query = """

                    UPDATE

                    [FinalProject].[dbo].[Flows] 

                    SET

                    UnixEndTimeMillisec = {},

                    counterOfPackets = {},

                    counterOfSyn = {},

                    counterOfPa = {},

                    counterOfR = {},

                    counterOfRA = {},

                    counterOfFin = {},

                    packetsTotalSize = {}

                    WHERE

                    FlowID={} and UnixStartTimeMillisec={}

                    """.format(flow["UnixEndTimeMillisec"],

                               newCounterOfPackets,

                               newCounterOfSyn,

                               newCounterOfPa,

                               newCounterOfR,

                               newCounterOfRA,

                               newCounterOfFin,

                               newSumOfFlowSize,

                               row[0], row[1]

                               )



                    curs.execute(query)

                    curs.commit()





                else:

                    #### there is no flow in the DB

                    query = """INSERT INTO  dbo.Flows values({},{},{},'{}',{},'{}','{}','{}',{},{},{},{},{},{},{},{},{},'{}',Null,Null)""".format(

                        flow["TimePeriod"],

                        flow["UnixStartTimeMillisec"],

                        flow["UnixEndTimeMillisec"],

                        flow["Day"],

                        flow["Time"],

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

                        flow["counterOfFin"],

                        flow["packetsTotalSize"],

                        ##########################
                        flow["PID"]
                        ##########################

                    )


                    try:
                        curs.execute(query)
                    except:
                        print (query)
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
             
             packetsTotalSize={}

             WHERE TimePeriod={}""".format(lastPacketCounting["endTimeUnixMillisec"], lastPacketCounting["packetCount"],
                                           lastPacketCounting["counterOfSyn"],
                                           lastPacketCounting["counterOfAck"],
                                           lastPacketCounting["counterOfPa"],
                                           lastPacketCounting["counterOfR"],
                                           lastPacketCounting["counterOfRA"],
                                           lastPacketCounting["counterOfFin"],
                                           lastPacketCounting["packetsTotalSize"],
                                           lastPacketCounting["TimePeriod"])

            curs.execute(query)

            curs.commit()



        except:

            query = """INSERT INTO  dbo.packetsCountTenSecond values({},{},{},'{}',{},{},{},{},{},{},{},{},Null,Null)""".format(
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
                lastPacketCounting["counterOfFin"],
                lastPacketCounting["packetsTotalSize"]
            )

            curs.execute(query)

            curs.commit()


    def insertPID(self,Processes):
        curs = self.conn.cursor()
        #### there is no flow in the DB
        for process in Processes:
            if(process['deltaTimeMillisec']!='None'):
                query="""SELECT PID FROM [FinalProject].[dbo].[Processes] Where (PID = '{}')""".format(process['pid'])
                curs.execute(query)
                if curs.rowcount!=0:
                    query = """UPDATE [FinalProject].[dbo].[Processes] SET deltaTimeMillisec = {} WHERE pid = '{}'""".format(process['deltaTimeMillisec'],process['pid'])
                else:
                    query = """INSERT INTO  dbo.Processes values('{}','{}','{}',{})""".format(
                        process['pid'],
                        process['fileName'],
                        process['filePath'],
                        process['deltaTimeMillisec']
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

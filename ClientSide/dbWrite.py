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
                                                                         r'PWD=Ll123456',
        autocommit=True
    )
    return connSQLServer


class Database():
    def __init__(self):
        self.conn = connectSQLServer(Driver, Server, DB)

    def insertDataTime(self, dataDict, curs):
        query = """INSERT INTO  dbo.Times values({},{},'{}','{}')""".format(dataDict["UnixTimeMicrosec"],
                                                                            dataDict["Time"],
                                                                            dataDict["Date"],
                                                                            dataDict["Day"])

        curs.execute(query)
        curs.commit()

    def insertDataPacket(self, dataDict, curs):
        query = """INSERT INTO  dbo.Packets values({},'{}','{}',{},{},{},{},{},{},'{}',{},{},{},'{}',{},{})""".format(
            dataDict["UnixTimeMicrosec"],
            dataDict["srcIpAddr"],
            dataDict["dstIpAddr"],
            dataDict["IPLen"],
            dataDict["ID"],
            dataDict["Ttl"],
            dataDict["IPChksum"],
            dataDict["srcPort"],
            dataDict["dstPort"],
            dataDict["service"],
            dataDict["Seq"],
            dataDict["Ack"],
            dataDict["dataOfs"],
            dataDict["Flags"],
            dataDict["Window"],
            dataDict["TcpChksum"]
        )

        curs.execute(query)
        curs.commit()


    def insertDataFile(self, dataDict, curs):
        query = """INSERT INTO  dbo.Files values({},{},'{}','{}',{})""".format(dataDict["UnixTimeMicrosec"],
                                                                            dataDict["PID"],
                                                                            dataDict["fileName"],
                                                                            dataDict["filePath"],
                                                                            dataDict["deltaTimeMillisec"])

        curs.execute(query)
        curs.commit()


    def insertData(self, dataDict):
        curs = self.conn.cursor()
        try:
            self.insertDataTime(dataDict, curs)
            self.insertDataPacket(dataDict,curs)
            if(dataDict["PID"]!='None'):
                if(dataDict["deltaTimeMillisec"]!="None"):
                    self.insertDataFile(dataDict,curs)
        except Exception as e:
            print(e)
            curs.rollback()

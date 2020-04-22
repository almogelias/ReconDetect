import pyodbc
import time
import sys

# SQL Parameters
Server = 'DESKTOP-GRTRD9G'
Driver = 'ODBC Driver 17 for SQL Server'
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

    def updatePackets10Sec(self, startTime,endTime,Day):
    #Write to DB
        time.sleep(30)
        curs = self.conn.cursor()
        query = """
        UPDATE [FinalProject].[dbo].[packetsCountTenSecond] SET SimulatorAttack=1 where (TimePeriod >= {} and TimePeriod < {}) and Day='{}'""".format(startTime,endTime,Day)
        curs.execute(query)
        self.conn.commit()


    def updateFlows(self, startTime,endTime,Day):
    #Write to DB
        time.sleep(10)
        cursor = self.conn.cursor()
        query = """UPDATE  [FinalProject].[dbo].[Flows] 
                            SET SimulatorAttack=1
                            where (TimePeriod >= {} and TimePeriod < {})
                            and Day='{}'""".format(startTime,endTime,Day)
        cursor.execute(query)
        self.conn.commit()


    def closeDbSession(self):
        self.conn.close()


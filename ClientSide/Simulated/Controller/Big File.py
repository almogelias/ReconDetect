import time
from random import randint
import sys
from dbWriteSimulations import Database
from datetime import datetime

####parameters####

tgt = sys.argv[1]
#PATH = '\\\\{}\\Share\\AnomallyFileTransfer\\'.format(tgt)
PATH = 'C:\\Scripts\\test\\'
fileSize = 100*int(sys.argv[2])


def dbWriteAsncProcess(startTimePeriod,endTimePeriod,day):
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod,endTimePeriod,day)
    conn.updateFlows(startTimePeriod,endTimePeriod,day)
    conn.closeDbSession()

def timePeriodCalc():
    now = datetime.now()
    current_time = int(now.strftime("%H%M%S"))
    return '{}'.format(current_time - current_time % 10)


########### Delay number between files ##########
############## 10 - 120 seconds ###########
def randomal():
    limit_time = 3
    n = randint(1, limit_time)
    return n

####### Ashkara Delay ###########
def delay(t):
    return time.sleep(t)

############ Random file size ##################
def randomSize(randomNum):
    return randomNum * 100

def create_file_size(file, nums_size):
    return file.truncate(nums_size)


counter = 0
print('     ###Starting bad files transfer###\n')
delay(2)
print('     ###Starting bad files transfer###')
delay_randomNum = randomal()
day = datetime.today().strftime("%A")
startTimePeriod = timePeriodCalc()
with open(r"{}BadFileTransfer-{}.txt".format(PATH, (str(time.time()))[:-3]), 'w') as f:
    #f.write("I'm a bad file, don't try to track me down!")
    create_file_size(f, fileSize)
    f.close()
    print("New bad file transferred: {} Bytes\n".format(fileSize))
print('\n###End bad files transfer###\n')
print('\n###End bad files transfer###\n')
endTimePeriod = str(int(timePeriodCalc()) + 10)

try:
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod, endTimePeriod, day)
    conn.updateFlows(startTimePeriod, endTimePeriod, day)
    conn.closeDbSession()
except Exception as e:
    print(e)

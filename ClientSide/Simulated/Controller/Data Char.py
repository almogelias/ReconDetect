import socket
from random import randint
import time
import sys
from dbWriteSimulations import Database
from datetime import datetime

Letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
tgt = sys.argv[1]
len_word=int(sys.argv[2])

def word():
    return_word = Letters[randint(0, len(Letters)-1)]
    return return_word

def sentence():
    return_sentence=''
    for length in range(randint(2,15)):
        return_sentence+=word()+' '
    return return_sentence.strip(' ')


def dbWriteAsncProcess(startTimePeriod,endTimePeriod,day):
    conn = Database()
    conn.updatePackets10Sec(startTimePeriod,endTimePeriod,day)
    conn.updateFlows(startTimePeriod,endTimePeriod,day)
    conn.closeDbSession()

def timePeriodCalc():
    now = datetime.now()
    current_time = int(now.strftime("%H%M%S"))
    return '{}'.format(current_time - current_time % 10)


def delay(t):
    return time.sleep(t)

if __name__ == '__main__':
    delay(4)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((str(tgt), 23))
    msg = word()
    day = datetime.today().strftime("%A")
    startTimePeriod = timePeriodCalc()
    client.send(msg.encode('utf-8'))
    from_server = client.recv(4096)
    client.close()
    endTimePeriod = str(int(timePeriodCalc()) + 10)
    print('Sent to Host :\n' + msg + ' - char has sent!')

    try:
        conn = Database()
        conn.updatePackets10Sec(startTimePeriod, endTimePeriod, day)
        conn.updateFlows(startTimePeriod, endTimePeriod, day)
        conn.closeDbSession()
    except Exception as e:
        print(e)


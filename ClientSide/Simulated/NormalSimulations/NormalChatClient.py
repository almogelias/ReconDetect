import socket
from random import randint
import time


Letters = 'abcdefghijklmnopqrstuvwxyz'



def word():

    return_word = ''

    for length in range(randint(1, 15)):

        return_word += Letters[randint(0, len(Letters)-1)]

    return return_word



def sentence():

    return_sentence=''

    for length in range(randint(2,10)):
        return_sentence+=word()+' '

    return return_sentence.strip(' ')


def delay(t):
    return time.sleep(t)



if __name__ == '__main__':

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('192.168.222.2', 21))



    while(True):
        delay(randint(1,10))
        msg = sentence().encode('utf-8')
        client.send(msg)
        from_server = client.recv(4096)
        print(from_server)

    client.close()

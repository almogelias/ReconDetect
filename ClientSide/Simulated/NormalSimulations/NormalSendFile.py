import time
from random import randint

####parameters####
PATH = '\\\\192.168.222.2\\Share\\NormalFileTransfer\\'


############ Delay number between files ##########
############## 10 - 120 seconds ###########
def randomal():
    limit_time = 120
    n = randint(10, limit_time)
    return n


####### Ashkara Delay ###########
def delay(t):
    return time.sleep(t)


############ Random file size ##################
def randomSize(randomNum):
    return randomNum * 10


def create_file_size(file, nums_size):
    return file.truncate(nums_size)


counter = 0
while (True):
    delay_randomNum = randomal()
    print(delay_randomNum)
    counter += delay_randomNum
    delay(delay_randomNum)
    with open(r"{}NormalFileTransfer-{}.txt".format(PATH, (str(time.time()))[:-3]), 'w') as f:
        # f.write("hihi test is it works?")
        create_file_size(f, randomSize(randint(1, 10)))
        print("NewFilePassed")

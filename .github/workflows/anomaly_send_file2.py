import time
from random import randint


####parameters####
############ Delay number between files ##########
############## 1- 3500 ###########
def randomal():
    limit_time = 20
    n = randint(1, limit_time)
    return n

####### Ashkara Delay ###########
def delay(t):
    return time.sleep(t)


############ Random file size ##################
def randomSize():
    return 1024*8000


def create_file_size(file, nums_size):
    return file.truncate(nums_size)


    #######################\\DESKTOP-GRTRD9G\test

delay_randomNum = randomal()
print(delay_randomNum)
delay(delay_randomNum)

for number in range(20):
    with open(r"D:\test\form-{}.txt".format(time.time()), 'w') as f:
        f.write("hihi test is it works?")
        create_file_size(f, randomSize())
        print("NewFilePassed")



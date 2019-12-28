import time
from random import randint


####parameters####
############ Delay number between files ##########
############## 0.1 - 5.0 ###########
def randomal():
    limit_time = 50
    n = randint(1, limit_time)
    n=n/10
    return n

####### Ashkara Delay ###########
def delay(t):
    return time.sleep(t)


############ Random file size ##################
def randomSize(random_one_to_four):
    if(random_one_to_four==1):
        return 10*1024
    elif(random_one_to_four==2):
        return 40*1024
    elif(random_one_to_four==3):
        return 100*1024
    elif (random_one_to_four == 4):
        return 140*1024
    elif (random_one_to_four == 5):
        return 247*1024
    elif (random_one_to_four == 6):
        return 138*1024
    elif (random_one_to_four == 7):
        return 1024*1024
    elif (random_one_to_four == 8):
        return 2457*1024
    elif (random_one_to_four == 9):
        return 3578*1024
    else:
        return 5784*1024


def create_file_size(file, nums_size):
    return file.truncate(nums_size)


    #######################\\DESKTOP-GRTRD9G\test
counter=0
while(counter<300):
    delay_randomNum = randomal()
    print(delay_randomNum)
    counter += delay_randomNum
    delay(delay_randomNum)
    with open(r"D:\test\form-{}.txt".format(time.time()), 'w') as f:
        f.write("hihi test is it works?")
        create_file_size(f, randomSize(randint(1, 10)))
        print("NewFilePassed")



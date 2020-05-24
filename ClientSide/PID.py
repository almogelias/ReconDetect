from collections import deque


class PID:
    def __init__(self):
        self.Processes=list()


    def AddProcess(self, dataDict):
        try:
            newProcess={
                'pid':dataDict['PID'],
                'fileName':dataDict['fileName'],
                'filePath':dataDict['filePath'],
                'deltaTimeMillisec':dataDict['deltaTimeMillisec']
            }
        except:
            newProcess = {
                'pid': dataDict['PID'],
                'fileName': 'None',
                'filePath': 'None',
                'deltaTimeMillisec': 0
            }
        checkIfExist = False
        if self.Processes:
            for id in self.Processes:
                if (id['pid']==newProcess['pid']):
                    checkIfExist = False
                    break
                else:
                    checkIfExist = True
                    continue
            if checkIfExist:
                self.Processes.append(newProcess)


        else:
            self.Processes.append(newProcess)

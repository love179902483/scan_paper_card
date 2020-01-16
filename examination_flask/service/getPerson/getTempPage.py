import os 
from config.pathVariable import PathVariable

class TempPage():  
    def __init__(self):
        self.batchNumbers = []

    def walkTempPage(self):
        utempPath = PathVariable().getTempPath()

        # for root, dirs, files in  os.walk(utempPath):
            # print(root)
            # print(dirs)
            # print(files)

        for file in os.listdir(utempPath):
            thisBatchNubmer = os.path.join(utempPath, file)
            self.batchNumber.append(thisBatchNubmer)

        if len(self.batchNumbers)!=0:
            for batchPath in self.batchNumbers:
                thisSanePath = os.listdir(batchPath)
                    
        else:
            print('无需要处理的批次信息!!!!!!!!!')
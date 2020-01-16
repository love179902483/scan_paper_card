from config.variable import SaneVariable
from config.pathVariable import PathVariable
import os
import ast

class PrepareSaneFile():
    '''
        准备扫描之前获取到本批次的信息，
        通过扫描的批次Number分别在 /utmp  与　/uploadImage　下创建 Number 文件夹
        通过扫描批次信息　在uploadImage下放入 variable.txt 
    '''
    def __init__(self):
        self.tempBatchPath = os.path.join(PathVariable.getTempPath(), SaneVariable.getBatchNumber())
        self.uploadBatchPath = os.path.join(PathVariable.getUploadPath(), SaneVariable.getBatchNumber())
        self.uploadBatchVariablePath = os.path.join(self.uploadBatchPath, 'variable.txt')
    def createFile(self):

        tempBatchFolder = os.path.exists(self.tempBatchPath)
        uploadBatchFolder = os.path.exists(self.uploadBatchPath)
        # uploadBatchVariable = os.path.exists(uploadBatchVariablePath)

        if not tempBatchFolder:
            os.makedirs(self.tempBatchPath) 

        if not uploadBatchFolder:
            os.makedirs(self.uploadBatchPath)

        # if not uploadBatchVariable:
        #     os.makedirs(uploadBatchVariablePath)

        print(self.uploadBatchVariablePath)

        # dic　转　str　为保存
        allVariable = str(SaneVariable.getSanVariable())
        try:
            file = open(self.uploadBatchVariablePath ,'w', encoding='utf-8')
            file.write(allVariable)
            file.close()
        except FileNotFoundError:
            print('不存在' + self.uploadBatchVariablePath)
        finally:
            file.close()

        

    def getVariableFromBatchFile(self):
        variableFile = open(self.uploadBatchVariablePath, 'r', encoding='utf-8')
        result = list()

        count = 0
        for line in variableFile.readlines():
            line = line.strip()
            if not len(line) or line.startswith('#'):
                continue
            
            if count == 0:
                getVariableDict = ast.literal_eval(line)
                # 将文件中的　variable　存入内存
                SaneVariable.setSanVariable(getVariableDict)
                print(getVariableDict) 
            count = count + 1
            break
import os

def getAllPictures(batchList, rootPath):
    '''
        获取所有要分析的图片并且返回一个map
        返回类型 map
        allPicturePath = {batchNumber: [[],[]]}
    '''
    allPicturePath = {}

    for batch in batchList:
        allPicturePath[batch] = []
        batchPath = os.path.join(rootPath, batch)

        for thisDir in os.listdir(batchPath):
            # print(thisDir)
            dirPath = os.path.join(batchPath, thisDir)
            if os.path.isdir(dirPath):
                filePathList = []
                for thisFile in os.listdir(dirPath):
                    filePath = os.path.join(dirPath, thisFile)
                    filePathList.append(filePath)
                if filePathList:
                    allPicturePath[batch].append(filePathList)

    return allPicturePath
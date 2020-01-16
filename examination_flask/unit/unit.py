
import os

# def createPagePath(dirPath, fileName):
#     '''
#         生成保存的文件地址
#     '''
#     finalPath = os.path.join(dirPath, fileName)
#     print(finalPath)
#     return finalPath



def createPageDir(aimPath):
    '''
        判断定义的 inventory　文件夹是否存在不存在则创建一个
    '''
    print(aimPath)
    
    if not os.path.exists(aimPath):
        os.makedirs(aimPath)
    
    return aimPath


def evaluateTolerance(a,b):
    '''
        计算容差   标准与opencv计算结果
    '''
    tolerance = 0 
    
    if a >= b:
        tolerance = round(b/a, 2)
    else :
        tolerance = round(a/b, 2)
    return tolerance

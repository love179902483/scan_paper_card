
import os

def deCodeRedisSet(mySet):
    '''
        将redis查出来的set类型值decode为 utf-8　并返回一个list
    '''
    myList = []
    for i in mySet:
        myList.append(i.decode('utf-8')) 

    return myList


def createPageDir(aimPath):
    '''
        判断定义的 inventory　文件夹是否存在不存在则创建一个
    '''
    # print(aimPath)
    
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

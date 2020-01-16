

import os
from config.redisConfig import RedisPool

class StatusVariable():
    Status = 0
    LastScannerStatus = 100

    @staticmethod
    def getStatusVariable():
        '''
            返回目前的状态
            0 就绪状态
            2 解析所有图片状态
            >100　扫描状态
        '''
        return StatusVariable.Status

    @staticmethod
    def setStatusVariable(status):


        '''
            设置目前状态
        '''
        if status == '1' :
            StatusVariable.Status = 100
        elif status == '2':
            StatusVariable.Status == 2
        elif status == '3':
            StatusVariable.Status == 3

    # @staticmethod
    # def compareScanner():
    #     if StatusVariable.Status > StatusVariable.LastScannerStatus:
            
        
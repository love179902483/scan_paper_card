
# -*- coding: utf-8 -*-

import os
from config.redisConfig import RedisPool

# 2479 ÷ 1240 = 2
# 3508 ÷ 1754 = 2
# 1240×1754
# shape 是(行，列)

SaneVariables_normal = {
    "BatchNumber": "33456",
    "Paper": {
        "shape": (1754, 1240),
        "width": 1240,
        "height": 1754,

        "paperName": "测试考试",
        "paperNumber": 123456,
        "testStudent": 222222,
        "saveDir": 'uploadImage'
    },
    "outFrame": {
        "width": 1175,
        "height": 1600,
        "circumference": 2*1175 + 1600*2,
        "area": 1175 * 1600,
        "tolerance": 0.85,
    },

    "PageFoot": {
        "startPoint": (0, 1531),
        "width": 1175,
        "height": 68,
        "pointWidth": 50,
        "pointHeight": 25,
        "allPages": 4,
    },
    # AllPages 是所有框子，包括习题，包括ＩＤ号
    # 每个框子都需要知道Ｙ轴的中心坐标．
    "AllPages": {
        "page1": {
            "MultipleChose": {

                "allStartPoint": (475, 25),
                "allWidth": 725,
                "allHeight": 550,
                # "shape": (562, 79), #可能有问题( 561.637, 79.113)

                "startPoint": (425, 25),
                "width": 675,
                "height": 550,
                "circumference": 2*675+550*2,
                "area": 550 * 675,
                "tolerance": 0.85,

                "pane": (50, 50),
                "paneArea": 50 * 50,
                "paneCircumference": 2*50+50*2,
                # （面积容差，周长容差）　容差:真实面积/标准面积
                "paneTolerance": (0.3, 0.5),
            },
            "ID": {
                # "shape": (562, 22), #可能有问题( 561.637, 21.576)
                "width": 350,
                "height": 500,
                "centerHeight": (50, 50),
                "circumference": 2*350+500*2,
                "area": 500*350,
                "tolerance": 0.85,

                "ratio": round(500/350, 2),  # 长宽的比例
                "pane": (50, 50),  # 可能有问题( 561.637, 21.576)
                "paneArea": 50*50,
                "paneCircumference": 50*2 + 50*2,
            },
            "subjective_01": {
                "startPoint": (0, 600),

                "width": 1175,
                "height": 400,
            },
            "subjective_02": {
                "startPoint": (0, 1000),
                
                "width": 1175,
                "height": 525,
            }
        }


    },
}


class SaneVariable():
    __SaneVariable = SaneVariables_normal

    @staticmethod
    def setToRedis(variable):
        expireTime = 30*24*60*60

        redisName_Paper = variable['BatchNumber'] + 'Paper'
        redisValue_Paper = str(variable['Paper'])

        redisName_OutFrame = variable['BatchNumber'] + 'OutFrame'
        redisValue_OutFrame = str(variable['outFrame'])

        redisName_PageFoot = variable['BatchNumber'] + 'PageFoot'
        redisValue_PageFoot = str(variable['PageFoot'])

        redisName_AllPages = variable['BatchNumber'] + 'AllPages'
        redisValue_AllPages = str(variable['AllPages'])
        
        redisPool = RedisPool.redisPool()

        result_Paper = redisPool.set(redisName_Paper, redisValue_Paper, expireTime)
        result_OutFrame =redisPool.set(redisName_OutFrame, redisValue_OutFrame, expireTime)
        result_PageFoot = redisPool.set(redisName_PageFoot, redisValue_PageFoot, expireTime)
        result_AllPages = redisPool.set(redisName_AllPages, redisValue_AllPages, expireTime)
        print(result_Paper ,result_OutFrame, result_PageFoot, result_AllPages)

        return result_AllPages and result_OutFrame and result_PageFoot and result_Paper

    @staticmethod
    def setSanVariable(variable):
        '''
            将本次 batch 数据 set 进入内存中
        '''
        SaneVariable.__SaneVariable = variable


    @staticmethod
    def getSanVariable_AllPapes_ByBatch(batchNumber):
        '''
            返回所有具体页数的数据
        '''
        redisPool = RedisPool.redisPool()
        return redisPool.get(batchNumber+'AllPages')

    @staticmethod
    def getSanVariable_Paper_ByBatch(batchNumber):
        '''
            返回本次扫描试卷的试题信息
        '''
        redisPool = RedisPool.redisPool()
        return redisPool.get(batchNumber+'Paper')

    @staticmethod
    def getSanVariableByBatch(batchNumber):
        '''
            返回本次扫描试卷纸张的外层黑框信息
        '''
        redisPool = RedisPool.redisPool()
        return redisPool.get(batchNumber+'OutFrame')

    @staticmethod
    def getSanVariableByBatch(batchNumber):
        '''
            返回本页的page页号的数据
        '''
        redisPool = RedisPool.redisPool()
        return redisPool.get(batchNumber+'PageFoot')





    @staticmethod
    def getSanVariable():
        '''
            返回扫描需要的所有数据
        '''
        return SaneVariable.__SaneVariable

    @staticmethod
    def getAllPages():
        '''
            返回所有具体页数的数据
        '''
        return SaneVariable.__SaneVariable['AllPages']

    @staticmethod
    def getPaper():
        '''
            返回本次扫描试卷的试题信息
        '''
        return SaneVariable.__SaneVariable["Paper"]

    @staticmethod
    def getOutFrame():
        '''
            返回本次扫描试卷纸张的外层黑框信息
        '''
        return SaneVariable.__SaneVariable["outFrame"]

    @staticmethod
    def getPageFoot():
        '''
            返回本页的page数据
        '''
        return SaneVariable.__SaneVariable["PageFoot"]

    @staticmethod
    def getBatchNumber():
        '''
            返回本页的page数据
        '''
        return SaneVariable.__SaneVariable["BatchNumber"]

# -*- coding: UTF-8 -*-

from config.redisConfig import RedisPool
from controll.analysisControll import getAllPersonMap
from controll.analysisControll import handleAllPersonMap
import logging



from myutil.util import deCodeRedisSet
import config.loggingConfig

if __name__ == "__main__":
    # 先模拟在redis中存入已经扫描好的文件夹 

    allScannerBatchList = RedisPool().redisPool().sinter('scannerList')
    allScannerBatchList = deCodeRedisSet(allScannerBatchList)
    print(allScannerBatchList)
    # RedisPool.redisPool().smove('scannerList', 'scannerListCopy')
    # for i in allScannerBatchList:
    #     allScannerBatchListCopy = RedisPool().redisPool().sadd('scannerListCopy', i)

    # print(allScannerBatchList)

    logging.debug('test')
    # 获取所有可处理图片的map
    allPersonMap = getAllPersonMap(allScannerBatchList)

    # 根据所有图片map处理图片
    handleAllPersonMap(allPersonMap)
    

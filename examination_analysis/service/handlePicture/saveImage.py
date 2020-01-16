
from config.redisConfig import RedisPool
import cv2

def imageToFile(imagePath, image):
    '''
        thisImagePath: 保存本地的时候的图片本地的保存路径
        saveKey: 保存本地的时候图片流
    '''
    print(imagePath)
    cv2.imwrite(imagePath, image)

def imageToRedis(redisKey,thisImagePath, saveKey):
    '''
        redisKey: 保存redis时候的外层key
        thisImagePath: 保存redis的时候的图片本地的保存路径
        saveKey: 保存redis的时候　map　的key
    '''
    RedisPool().redisPool1().hset(redisKey, saveKey, thisImagePath)

def answerToRedis(redisKey, answer):
    '''
        redisKey: 保存redis时候的外层key
        answer: 保存redis的时候所有answer
    '''
    RedisPool().redisPool1().hset(redisKey, 'MultipleChose', str(answer))

def idToRedis(redisKey, ID):
    '''
        redisKey: 保存redis时候的外层key
        ID: 保存redis的时候的学号
    '''
    RedisPool().redisPool1().hset(redisKey, 'ID', ID)


def batchToRedis(redisKey, batchID):
    '''
        保存学号到redis;
        redisKey: 保存redis时候的外层key;
        batchID: 保存redis的时候的batch ID号
    '''
    RedisPool().redisPool1().hset(redisKey, 'batch', batchID)
    

from service.prepare.getAllPic import getAllPictures
from config.pathVariable import PathVariable
from service.handlePicture.handle import handleThisPicture
from service.handlePicture import saveImage
from myutil import util
import logging
import cv2
import os

def getAllPersonMap(allBatchList):

    # 获取所有可以处理的图片并以本批次为key组合成map    
    allPictureMap = getAllPictures(allBatchList, PathVariable().getTempPath())
    logging.info('获取所有图片地址')
    logging.info(allPictureMap)
    return allPictureMap


def handleAllPersonMap(allPersonMap):
    for batch, pictures in allPersonMap.items():
        for picturePathList in pictures:
            allImage = {}         
            logging.info('本文件夹下所有图片 %s'% str(picturePathList))
            # 获取到每一个文件的图片
            for picturePath in picturePathList:
                logging.info('处理本张图片  "%s"' % picturePath)
                getResult = handleThisPicture(picturePath, batch)
                print(getResult['flag'])
                if getResult['flag']:
                    allImage = dict(allImage, **getResult['data'])
                else :
                    logging.error('处理的图片返回flag为False %s' % str(getResult))
                    continue
            # 保存所有的图片
            # logging.info(allImage)

          
            logging.info('得到所有的获取到的所有key:%s'% str(allImage.keys()))
            # print(allImage)
            print('ID' in allImage.keys())
            if 'ID' in allImage.keys():
                logging.info('获取到的学号ID:%s'% allImage['ID'])
                # 先确定好存redis的key = batch+ID
                redisID = str(batch) + str(allImage['ID'])
                for i in allImage:
                    if i == 'ID':
                        saveImage.idToRedis(redisID, allImage['ID'])
                        saveImage.batchToRedis(redisID, batch)
                        continue
                    elif i == 'MultipleChose':
                        # 保存到redis中选择题结果
                        saveImage.answerToRedis(redisID, allImage['MultipleChose'])
                        continue
                    else:
                        # 图片要保存的文件夹路径
                        savePath = os.path.join(PathVariable().getUploadPath(), str(allImage['ID']))
                        # 先确定文件夹是否存在若不存在则创建
                        util.createPageDir(savePath)
                        # 本张图片要保存的路径
                        imagePath = os.path.join(savePath, i + '.jpeg')
                        # 先保存图片，再将路径存到redis
                        saveImage.imageToFile(imagePath, allImage[i])
                        saveImage.imageToRedis( redisID, imagePath, i)
            else:
                logging.error('扫描出来的图片无ＩＤ号！ "%s"'% str(picturePathList))
                print(picturePathList + '扫描出来的无ＩＤ号！！！！')
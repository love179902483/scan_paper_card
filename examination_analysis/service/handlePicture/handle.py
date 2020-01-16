
# -*- coding: UTF-8 -*-
from service.getPerson.getOutFrameService import GetOutFrame
from service.getPerson.getThisPaperPage import GetPaperPage
from config.redisConfig import RedisPool
from service.getPerson.transferAndCut import TransferAndCut

import cv2
import ast

def handleThisPicture(picturePath, batch):
    # standardImg 
    # outFrameValue
    returnMsg = {'flag': False, 'msg':'', 'data': {}}

    try:
        paperInfoStr = RedisPool().redisPool().get(batch+'Paper')
        paperInfoMap = ast.literal_eval(paperInfoStr.decode('utf-8')) 

        outFrameInfoStr = RedisPool().redisPool().get(batch+'OutFrame')
        outFrameInfoMap = ast.literal_eval(outFrameInfoStr.decode('utf-8')) 

        pageFootInfoStr = RedisPool().redisPool().get(batch+'PageFoot')
        pageFootInfoMap = ast.literal_eval(pageFootInfoStr.decode('utf-8')) 

        AllPagesInfoStr = RedisPool().redisPool().get(batch+'AllPages')
        AllPagesInfoMap = ast.literal_eval(AllPagesInfoStr.decode('utf-8')) 
    except Exception as error:
        print(error)
        returnMsg['msg'] = '在redis中缺少对应 '+ batch +' 的答题卡信息!!!!'
        return returnMsg
    

    try:
        outFrame = GetOutFrame(picturePath, paperInfoMap, outFrameInfoMap)
        standardPicture = outFrame.init()
        standardPictureGray = cv2.cvtColor(standardPicture, cv2.COLOR_BGR2GRAY)

    except Exception as error:
        returnMsg['msg'] = batch +'批次下,解析图片出错!!!!'
        return returnMsg


    try:
        # 获取页数
        getPaperPage = GetPaperPage(standardPicture, pageFootInfoMap)
        page = getPaperPage.getPage()
        print(page)
    except Exception as error:
        returnMsg['msg'] = '获取'+ batch +'下的　page　出错!!!!!'
        return returnMsg

    try:
        print(AllPagesInfoMap)
        # 开始切割图片之后　根据获取到的学号ID保存图片
        transferCut = TransferAndCut(standardPictureGray, AllPagesInfoMap, page)
        return transferCut.getAllImages()
    except Exception as error:
        returnMsg['msg'] = batch +'批次下,切割图片出错'
        return returnMsg


    # try:
    #     pass
    # except Exception as error:
    #     pass

    # returnMsg['flag'] = True;
    # returnMsg['picture'] = standardPicture

    # return returnMsg


    
    # cv2.imshow('test', standardPicture)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    

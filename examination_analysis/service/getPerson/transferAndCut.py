
import cv2
import numpy as np
import logging


class TransferAndCut():
    '''
    转换得到的图片并且切割开
    获取到的标准外框信息进行处理和切割
    根据页数，获取该页的参数信息，并进行切割
    imageGray 原图片的灰度图
    pageData 　所有页的参数信息
    page    本页的页码数
    '''
    def __init__(self, imageGray, pageData, page):
        self.page = page
        self.imageGray = imageGray
        self.pageData = pageData
        # 本页纸张的对应的标准 data　数据
        self.thisPageData = {}

    def getAllImages(self):
        '''
            获取所有的小图片
        '''
        self.__getThisPageData()
        returnData = self.__cutImageFromVariable()
        # print(returnData)
        return returnData
    

    def __handleImage(self, ImageGray):
        
        #高斯滤波
        img_GaussianBlur=cv2.GaussianBlur(ImageGray,(15,15),0)

        # 获取二值图像
        _,img_threshold = cv2.threshold(img_GaussianBlur, 127, 255, cv2.THRESH_BINARY_INV)
        
        # 开闭运算的滑块
        kernel = np.ones((15,15),np.uint8)
        # 开闭运算
        img_opening = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, kernel,iterations=1)

        # 获取轮廓结果
        contours, hierarchy = cv2.findContours(img_opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        return contours


    def __calculateResult(self, contours, variable, situation):
        '''
            contours 获取到的所有外层框子
            variable 标准的变量
            situation 是否是计算ＩＤ   0：计算ＩＤ    1：计算选择题

            返回值　answer: (题号, [选项])
        '''

        standardWidth = variable['width']
        standardHeight = variable['height']
        standardArea = variable['area']
        standardLength = variable['circumference']
        standardPane = variable['pane']
        standardPaneArea = variable['paneArea']
        standardPaneLength = variable['paneCircumference']
        standardPaneTolerance = variable['paneTolerance']
        standardPaddingLeft = variable['padding_left'] if 'padding_left' in variable.keys() else 0
        standardPaddingTop = variable['padding_top']  if 'padding_top' in variable.keys() else 0

        allAnswer = {}

        print(len(contours))
        # print(contours)

        count = 0
        for contour in contours:
            # 计算本框框面积
            realArea = cv2.contourArea(contour)
            # 计算本框框周长
            realLength = cv2.arcLength(contour,True)
            realToleranceAreaTolerance = round(realArea/standardPaneArea, 2)
            realToleranceLengthTolerance = round(realLength/standardPaneLength, 2)

            # print('GOT RESULT [REAL]: ')
            # print(realArea, realLength)
            # print('GOT RESULT　［TOLERANCE］: ')
            # print(realToleranceAreaTolerance, realToleranceLengthTolerance) 
            # print(standardPaneTolerance)

            # 若获取到的容差在　容差范围之内则开始计算题的答案
            if standardPaneTolerance[0] <= realToleranceAreaTolerance <= 1.1 and standardPaneTolerance[1] <= realToleranceLengthTolerance <= 1.1:
                count = count + 1
                M = cv2.moments(contour)
                if M['m00'] != 0 :
                    # 得到符合标准的中心点 x ,y 为 cx ,cy
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                    if situation == 0:
                        paneNumber = int((cx - standardPaddingLeft) / standardPane[0]) 
                        paneAnswer = int((cy - standardPaddingTop) / standardPane[1]) 

                    elif situation == 1:
                        if cy > standardPane[1]*6:
                            paneNumber = int((cx - standardPaddingLeft) / standardPane[0]) + 13
                            paneAnswer = int((cy - standardPane[1] * 6 - standardPaddingTop) / standardPane[1]) + 1

                        else: 
                            paneNumber = int((cx - standardPaddingLeft) / standardPane[0]) + 1
                            paneAnswer = int((cy - standardPane[1] - standardPaddingTop * 6) / standardPane[1]) + 1


                    # 判断　dict 中是否有这个key如果有则将 answer 放入如果没有则　赋值
                    if paneNumber in allAnswer.keys():
                        allAnswer[paneNumber].append(paneAnswer)
                    else:
                        allAnswer[paneNumber] = [paneAnswer]
                    
                    # print(allAnswer)

                    # MultipleResult[paneNumber].append(paneAnswer)
        print(count)
        allAnswer = sorted(allAnswer.items(), key=lambda item: item[0])
 
        return allAnswer

    def __getImageStudentID(self, variable):
        '''
            获取标准的学号框子
            variable 学号的 dict　值
        '''
        startY = variable['startPoint'][1]
        startX = variable['startPoint'][0]
        endY = startY + variable['height']
        endX = startX + variable['width']
        # 处理图片获取切割后的图片用于保存
        ImageGray_StudentID = self.imageGray[startY: endY , startX: endX]
        # 处理图片获取要处理的点----二值图像，获取到所有的点用于获取学号
        resultContours = self.__handleImage(ImageGray_StudentID)

        # cv2.drawContours(ImageGray_StudentID, resultContours, -1, (255, 0, 255), 1)
        # cv2.imshow('test', ImageGray_StudentID)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 处理图片获取最终的学号，级学号的框子
        allAnswer = self.__calculateResult(resultContours, variable, 0)
        
        # 将[(1, [4]), (2, [6]), (3, [7]), (4, [6]), (5, [7]), (6, [4]), (7, [8])]类型的数据转为字符串4676748
        returnAnswer = ''

        for i in allAnswer:
            returnAnswer = returnAnswer + returnAnswer.join(str(x) for x in i[1])

        # logging.info('获取学号' + returnAnswer)
        # 根据key 排序
        
        return returnAnswer, ImageGray_StudentID

        
    def __getImageMultipleChose(self, variable):
        '''
            获取标准的学号框子
            variable 选择题 dict　值
        '''
        startY = variable['startPoint'][1]
        startX = variable['startPoint'][0]
        endY = startY + variable['height']
        endX = startX + variable['width']

        # 处理图片获取切割后的图片用于保存
        ImageGray_Multiplechoose = self.imageGray[startY: endY , startX: endX] 
        # 处理图片获取要处理的点----二值图像，获取到所有的点用于获取学号
        resultContours = self.__handleImage(ImageGray_Multiplechoose)
        # 处理图片获取最终选择题答案，及答案的框子
        allAnswer = self.__calculateResult(resultContours, variable, 1)
        

        print('获取选择题答案' + str(allAnswer))
        return allAnswer, ImageGray_Multiplechoose

    def __getOtherImage(self, variable):
        '''
            获取普通的框子，直接切割
        '''
        startY = variable['startPoint'][1]
        startX = variable['startPoint'][0]
        endY = startY + variable['height']
        endX = startX + variable['width']
        ImageGray = self.imageGray[startY: endY , startX: endX]

        return ImageGray

    def __cutImageFromVariable(self):

        '''
            解析变量，获取学生ID信息
            若这一页有ID的信息则要处理
            并且获取所有这一页的所有小图片
        '''
        returnMsg = {
            'flag': True,
            'data':{},
            'msg': '',
        }

        # 每一页的所有小图片
        for key, value in self.thisPageData.items():

            if key == 'ID':
                answer, imageGray = self.__getImageStudentID(value)
                # 若答案的长度与传入的标准长度一致则表示ＯＫ
                if len(answer) == value['length']:
                    returnMsg['data'][key] = answer
                    returnMsg['data'][key+"_image"] = imageGray
                else:
                    returnMsg['flag'] = False
                    returnMsg['msg'] = 'ID位数有问题目前为' + str(len(answer)) 

            elif key == 'MultipleChose':
                answer, imageGray = self.__getImageMultipleChose(value)
                returnMsg['data'][key] = answer
                returnMsg['data'][key+"_image"] = imageGray
            else:
                imageGray = self.__getOtherImage(value)
                returnMsg['data'][key] = imageGray

        return returnMsg

        # return returnValue


    def __getThisPageData(self):
        '''
            通过传入的page参数获取本页的数据信息
        '''
        key = 'page'+str(self.page)

        self.thisPageData = self.pageData[key]

    
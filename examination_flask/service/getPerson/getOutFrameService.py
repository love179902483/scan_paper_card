from config import pathVariable
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from unit import unit

class GetOutFrame():
    def __init__(self, paperInfo, outFrameInfo):
        '''
        paperInfo: 纸张信息
        outFrameInfo: 外部轮廓信息
        '''
        # self.paperData = paperData
        self.paperInfo = paperInfo
        self.outFrameInfo = outFrameInfo
        # 获取 temp 文件夹位置
        self.tempPath = pathVariable.PathVariable.getTempPath()
        # 获取 uploadImage 文件夹位置 
        self.uploadPath = pathVariable.PathVariable.getUploadPath()
        # 保存所有 temp　下的文件路径
        self.__allTempPicturePath = [] 

        # 标准外框的面积
        self.standardOutFrameArea = outFrameInfo['area']
        # 标准外框的周长
        self.standardOutFrameLength = outFrameInfo['circumference']
        # 标准外框与实际外框的容差
        self.standardOutFrameTolerance = outFrameInfo['tolerance']
        # 标准外框的高度
        self.standardOutFrameHeight = outFrameInfo['height']
        # 标准外框的宽度 
        self.standardOutFrameWidth = outFrameInfo['width']
        
    def init(self):
        # 将所有遍历出来的图片保存到 self.__allTempPicture 变量中
        self.__getAllTemp()
        # 重新计算获取A4大小比例的纸张
        self.__reshapeToStandard()

        # 截取第一张图片的信息,通过仿射变换获取正矩形
        return self.__getThiOutFrame(self.allTempPicture[0])

    @property
    def allTempPicture(self):
        self.__getAllTemp() 
        return self.__allTempPicturePath

    def __getAllTemp(self):
        for root, dirs, files in  os.walk(self.tempPath):
            for pictureName in files:
                self.__allTempPicturePath.append(os.path.join(root, pictureName))
        # return self.allTempPicture


    def __reshapeToStandard(self):

        for thisImgPath in self.__allTempPicturePath:
            thisImg = cv2.imread(thisImgPath)

            standardHeight = self.paperInfo['height']
            standardWidth = self.paperInfo['width']

            thisImageHeight = thisImg.shape[0]
            thisImageWidth = thisImg.shape[1]

            # 以图片高度为准，计算图片的宽度
            thisImageReshape = ( int((standardHeight/thisImageHeight)*thisImageWidth), standardHeight)
            # resize图片
            thisImg = cv2.resize(thisImg, thisImageReshape, interpolation=cv2.INTER_CUBIC)
            # 保存resize之后的图片
            cv2.imwrite(thisImgPath, thisImg)
           
    def __getThiOutFrame(self, imgPath):
        '''
        获取最外层大框子

        imgPath: 传入的图片路径。   
        
        result：　bgr三通道图片，标准的正矩形，外框图片
        '''
        thisImg = cv2.imread(imgPath)
        thisImg_gray = cv2.cvtColor(thisImg, cv2.COLOR_BGR2GRAY)

        # 高斯滤波
        blur = cv2.GaussianBlur(thisImg_gray, (5,5), 0)

        # Canny算子求得图像边缘
        edges = cv2.Canny(blur, 70, 150, apertureSize = 3)

        # 闭运算 线膨胀后腐蚀
        kernel = np.ones((10,10),np.uint8)
        closing = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)

        # 寻找轮廓
        contours, hier = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # 接收最大匹配的轮廓
        maxTorleracnePoints = [[], 0]


        for point in contours:
            rect = cv2.minAreaRect(point)

            # 找质心，面积，周长用到
            M = cv2.moments(point)
            #（x,y）为矩形左上角的坐标，（w,h）是矩形的宽和高
            
            # 计算本框的矩形面积
            thisPointArea = cv2.contourArea(point)
            # 计算本框框面积容差
            toleranceResultArea = unit.evaluateTolerance(thisPointArea, self.standardOutFrameArea)
            # 计算本框框周长
            thisPointLength = cv2.arcLength(point,True)
            # 计算周长容差
            toleranceResultLength = unit.evaluateTolerance(self.standardOutFrameLength, thisPointLength)

            # 周长、面积、以及中心点高度必须达到容差要求才算是合格
            # M['m00'] != 0 and toleranceResultArea >= standardAimTolerance and toleranceResultLength >= standardAimTolerance
            if M['m00'] != 0 and toleranceResultArea >= self.standardOutFrameTolerance and toleranceResultLength >= self.standardOutFrameTolerance: 
                
                print(toleranceResultArea, toleranceResultLength)

                if maxTorleracnePoints[1] < toleranceResultLength:

                    maxTorleracnePoints = [point, toleranceResultLength]

        approx = cv2.approxPolyDP(maxTorleracnePoints[0], 0.05 * self.standardOutFrameLength, True)

        rect = cv2.minAreaRect(maxTorleracnePoints[0])  
        box = cv2.boxPoints(rect)
        # print(str(box))

        # 先平方和 确定出 左上角以及右下角的值
        box = sorted(box, key=lambda x: x[0]**2 + x[1]**2)
        # 判断中间两个元素的横坐标值，如果第二个 < 第三个　则交换顺序
        if box[1][0] < box[2][0]: box[1],box[2] = box[2], box[1]
        # 最后交换第三个元素和第四个元素的值, 最后四个点的顺序为左上，右上，右下，左下
        box[2],box[3] = box[3], box[2]
        
        #　将获取的小数转换为整数
        for point in box:
            point[0] = round(point[0])
            point[1] = round(point[1])


        #根据四个顶点设置图像透视变换矩阵
        pos1 = np.float32(box)
        pos2 = np.float32([[0, 0],[self.standardOutFrameWidth, 0], [self.standardOutFrameWidth, self.standardOutFrameHeight], [0, self.standardOutFrameHeight]])
        M1 = cv2.getPerspectiveTransform(pos1, pos2)
        #图像透视变换,最终返回正矩形
        resultPage = cv2.warpPerspective(thisImg, M1, (self.standardOutFrameWidth, self.standardOutFrameHeight))
        
        
        return resultPage


        # print(str(box))
        # box = np.int0(box)
        # print(pos1)
        # print(pos2)



        # cv2.drawContours(thisImg, [box], 0, (0,0,225), 5) 
        # # cv2.drawContours(thisImg, contours, -1, (0, 0, 255), 1)

        # # plt.imshow(blur)
        # # plt.show()
        # print(result.shape)
        # # cv2.imshow('hehe', thisImg_gray)
        # cv2.namedWindow('hehe',0)
        # cv2.imshow('hehe', result)
        # cv2.waitKey(0)

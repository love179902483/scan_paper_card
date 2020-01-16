
import cv2
import numpy as np
from unit.unit import evaluateTolerance

class GetPaperPage():
    '''
    根据获取这一页的标准外框获取页数，
    每页标志页数的框子位置必须固定
    '''
    def __init__(self, thisImage,  pageVariable):
        '''
            thisImage 灰度图
            pageVariable　纸张的信息
        '''
        # 每页的页码信息
        self.pageStartPoint = pageVariable['startPoint']
        self.width = pageVariable['width']
        self.height = pageVariable['height']
        self.pagePointWidth = pageVariable['pointWidth']
        self.pagePointHeight = pageVariable['pointHeight']
        self.pagePointArea = pageVariable['pointWidth'] * pageVariable['pointHeight']
        self.pagePointLength = pageVariable['pointWidth'] * 2 + pageVariable['pointHeight'] * 2
        self.allPages = pageVariable['allPages']

        #　目标灰度图
        # self.image = thisImage
        self.imageGray = thisImage

        # 接收页码的点坐标，必须只有３个
        self.pagePoint= []
        self.page = 0

    # def init(self):
    #     self._getPage()

    def getPage(self):
        print(self.imageGray.shape)
        rowStart = self.pageStartPoint[1]
        rowEnd = self.pageStartPoint[1] + self.height
        columnStart = self.pageStartPoint[0]
        columnEnd = self.pageStartPoint[0] + self.width

        print(rowStart, rowEnd, columnStart, columnEnd)
        pageImage = self.imageGray[rowStart: rowEnd, columnStart: columnEnd]
        print(pageImage.shape)

        #高斯滤波
        img_GaussianBlur=cv2.GaussianBlur(pageImage,(11,11),0)

        # 获取二值图像
        _,img_threshold = cv2.threshold(img_GaussianBlur, 127, 255, cv2.THRESH_BINARY_INV)
        
        # 开闭运算的滑块
        kernel = np.ones((20,20),np.uint8)
        # 开闭运算
        img_opening = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, kernel,iterations=1)
        # 获取轮廓结果
        contours, hierarchy = cv2.findContours(img_opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        allContoursCenter = []
        try:
            for contour in contours:
                print(len(contours))
                # 计算本框框面积
                realArea = cv2.contourArea(contour)
                # 计算本框框周长
                realLength = cv2.arcLength(contour,True)

                # 计算其容差是否符合标准

                if 0.3 < evaluateTolerance(realArea, self.pagePointArea) and 0.3 < evaluateTolerance(realLength, self.pagePointLength):
                    M = cv2.moments(contour)
                    if M['m00'] != 0 :
                        # 得到符合标准的中心点 x ,y 为 cx ,cy
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        thisPointCenter = (cx, cy)
                        allContoursCenter.append(thisPointCenter)

            # 定义page的页码个数必须是３个
            if len(allContoursCenter) == 3:
                allContoursCenter = sorted(allContoursCenter, key=lambda x: x[0])
                self.pagePoint = allContoursCenter
                

        except Exception as error:
            print(error)

        # 计算页码,看中间的横坐标位于 n/m中
        pagePointAllWidth = self.pagePoint[2][0] - self.pagePoint[0][0]
        pagePointWidth = self.pagePoint[1][0] - self.pagePoint[0][0]
        # 页码单位长度　总长度/页码数
        pageUnitWidth = pagePointAllWidth / self.allPages

        self.page = int(pagePointWidth/pageUnitWidth) + 1

        return 1

        # print('page：' + str(self.page))
        # cv2.namedWindow('test',0)
        # cv2.imshow('test', img_opening)
        # cv2.waitKey(0)
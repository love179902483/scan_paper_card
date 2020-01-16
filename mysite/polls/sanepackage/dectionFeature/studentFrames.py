import cv2
import numpy as np

from polls.sanepackage.dectionFeature import kerasLoad

def getStandardDetails(frameFeatures):
    '''
        return
        标准纸张信息, 标准选择题框子的信息, 标准学号框子的信息
    '''
    print(frameFeatures)
    print('framefeatures---------------------')
    for i in frameFeatures.keys():
        print(i)
    print('framefeatures---------------------')
    paper = frameFeatures['Paper']
    multipleQuestionFrame = frameFeatures['AllFrames']['MultipleChose']
    studentIDFrame = frameFeatures['AllFrames']['ID']
    outFrame = frameFeatures['outFrame']

    return paper, multipleQuestionFrame, studentIDFrame, outFrame


def getOutFrame(img, outFrameStandard):
    '''
    获取最外层大框子

    img: 传入的扫描图片。   outFrameStandard：　标准的外框信息
    
    result：　bgr三通道图片，标准的正矩形，外框图片
    '''
    # 标准的面积
    standardAimArea = outFrameStandard['area']
    # 标准周长
    standardAimLength = outFrameStandard['circumference']
    # 标准的容差
    standardAimTolerance = outFrameStandard['tolerance']
    # 标准高度（外层框子）
    standardHeight = outFrameStandard['height']
    # 标准宽度（外层框子）
    standardWidth = outFrameStandard['width']
    # 标准Y值范围 (min, max)
    # standardAimHeightRange = outFrameStandard['centerHeight']

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # 中值滤波 过滤噪声，保留边缘信息
    # gray = cv2.medianBlur(gray,1) 
    # 双边滤波
    # blur =  cv2.bilateralFilter(img,9,75,75)
    # 高斯滤波
    # blur =  cv2.GaussianBlur(img,(5,5),0)

    # Canny算子求得图像边缘
    edges = cv2.Canny(gray, 70, 150, apertureSize = 3)

    # 闭运算 线膨胀后腐蚀
    kernel = np.ones((3,3),np.uint8)
    closing = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)

    # 寻找轮廓
    contours, hier = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # # 获取面积最大的contour
    # cnt = max(contours, key=lambda cnt: cv2.contourArea(cnt))
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 1)


    # 接收最大匹配的轮廓
    maxTorleracnePoints = [[], 0]
    for point in contours:
        # 找质心，面积，周长用到
        M = cv2.moments(point)
        #（x,y）为矩形左上角的坐标，（w,h）是矩形的宽和高
        
        # 计算本框框的面积
        thisPointArea = cv2.contourArea(point)
        # 计算本框框面积容差
        toleranceResultArea = evaluateTolerance(thisPointArea, standardAimArea)
        # 计算本框框周长
        thisPointLength = cv2.arcLength(point,True)
        # 计算周长容差
        toleranceResultLength = evaluateTolerance(standardAimLength, thisPointLength)

        # 周长、面积、以及中心点高度必须达到容差要求才算是合格
        # M['m00'] != 0 and toleranceResultArea >= standardAimTolerance and toleranceResultLength >= standardAimTolerance
        if M['m00'] != 0 and toleranceResultArea >= standardAimTolerance and toleranceResultLength >= standardAimTolerance: 
            
            print(toleranceResultArea, toleranceResultLength)

            if maxTorleracnePoints[1] < toleranceResultLength:

                maxTorleracnePoints = [point, toleranceResultLength]

                # print('Got outFrame and this toleranceLength： {length} ; toleranceArea： {area} '.format(length=toleranceResultLength, area=toleranceResultArea))
                # cx = int(M['m10']/M['m00'])
                # cy = int(M['m01']/M['m00'])
                # 中心点高是否合格
                # print(toleranceResultArea)
                # print(thisPointArea)
               
                # print('中心点',(cx, cy))
                # print(point)
                # cv2.drawContours(img, [point], -1, (0, 0, 255), 1)
                # x,y,w,h=cv2.boundingRect(point)
                # img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)

    approx = cv2.approxPolyDP(maxTorleracnePoints[0], 0.05 * standardAimLength, True) 
    cv2.drawContours(img, [approx], -1, (0, 0, 255), 1)

    # 先平方和 确定出 左上角以及右下角的值
    approx = sorted(approx, key=lambda x: x[0][0]**2 + x[0][1]**2)
    # 判断中间两个元素的横坐标值，如果第二个 < 第三个　则交换顺序
    if approx[1][0][0] < approx[2][0][0]: approx[1],approx[2] = approx[2], approx[1]
    # 最后交换第三个元素和第四个元素的值
    approx[2],approx[3] = approx[3], approx[2]


    print('这个是外层的框子')
    print(approx)
    # print(outFrameStandard)
    #根据四个顶点设置图像透视变换矩阵
    pos1 = np.float32(approx)
    pos2 = np.float32([[0, 0],[standardWidth, 0], [standardWidth, standardHeight], [0, standardHeight]])
    M1 = cv2.getPerspectiveTransform(pos1, pos2)
    #图像透视变换,最终返回正矩形
    result = cv2.warpPerspective(img, M1, (standardWidth, standardHeight))

    print('打印标记的图片')
    # cv2.imshow('1', result)
    # cv2.imshow('2', closing)
    # cv2.imshow('3',edges)
    # cv2.waitKey(0)  
    # cv2.destroyAllWindows()

    return result


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

def getStudentIDPoints(img, studentFrameStandard):
    print('studentID 框子')
    print(img.shape)
    # 标准的面积
    standardAimArea = studentFrameStandard['area']
    # 标准周长
    standardAimLength = studentFrameStandard['circumference']
    # 标准的容差
    standardAimTolerance = studentFrameStandard['tolerance']
    # 标准Y值范围 (min, max)
    standardAimHeightRange = studentFrameStandard['centerHeight']

    # print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = img

    # 中值滤波 过滤噪声，保留边缘信息
    # gray = cv2.bilateralFilter(gray,3,21,21) 


    # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    # dst = cv2.filter2D(gray, -1, kernel=kernel)

    # Laplacian算子
    # dst = cv2.Laplacian(gray, cv2.CV_16S, ksize = 3)
    # dst = cv2.convertScaleAbs(dst) 

    # Sobel算子
    # x = cv2.Sobel(gray, cv2.CV_16S, 1, 0) #对x求一阶导
    # y = cv2.Sobel(gray, cv2.CV_16S, 0, 1) #对y求一阶导
    # absX = cv2.convertScaleAbs(x)      
    # absY = cv2.convertScaleAbs(y)    
    # dst = cv2.addWeighted(absX, 0.2, absY, 0.2, 0)




    #Prewitt算子
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],dtype=int)
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=int)
    x = cv2.filter2D(gray, cv2.CV_16S, kernelx)
    y = cv2.filter2D(gray, cv2.CV_16S, kernely)

    #转uint8
    absX = cv2.convertScaleAbs(x)       
    absY = cv2.convertScaleAbs(y)    
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0)


    # Canny算子求得图像边缘
    edges = cv2.Canny(dst, 50, 150, apertureSize = 3)

    # 闭运算 线膨胀后腐蚀
    # kernel = np.ones((5,5),np.uint8)
    # closing = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)

    # 寻找轮廓
    contours, hier = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # # 获取面积最大的contour
    # cnt = max(contours, key=lambda cnt: cv2.contourArea(cnt))

    cv2.drawContours(img, contours, -1, (255, 0, 255), 1)

    count = 0
    for point in contours:
        # 找质心，面积，周长用到
        M = cv2.moments(point)
        #（x,y）为矩形左上角的坐标，（w,h）是矩形的宽和高
        
        # 计算本框框的面积
        thisPointArea = cv2.contourArea(point)
        # 计算本框框面积容差
        toleranceResultArea = evaluateTolerance(thisPointArea, standardAimArea)
        # 计算本框框周长
        thisPointLength = cv2.arcLength(point,True)
        toleranceResultLength = evaluateTolerance(standardAimLength, thisPointLength)
        if toleranceResultLength > 0.8 and toleranceResultArea > 0.3:
            approx = cv2.approxPolyDP(point, 0.05 * standardAimLength, True) 
            count = count + 1
            cv2.drawContours(img, [point], -1, (0, 255, 255), 1)
        # 周长、面积、以及中心点高度必须达到容差要求才算是合格
        # M['m00'] != 0 and toleranceResultArea > standardAimTolerance and toleranceResultLength > standardAimTolerance
        if M['m00'] != 0 and toleranceResultArea > standardAimTolerance and toleranceResultLength > standardAimTolerance:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(img, [point], -1, (255, 0, 255), 1)
            # 中心点高是否合格
            if  standardAimHeightRange[0] < cy < standardAimHeightRange[1]:
                print(toleranceResultArea)
                print(thisPointArea)
                print('中心点',(cx, cy))
                # count = count + 1
                # print(point)
                cv2.drawContours(img, [point], -1, (0, 0, 255), 1)
                # x,y,w,h=cv2.boundingRect(point)
                # img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
    
    print('共找到count个', count)
    
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 1)、

    cv2.imshow('1', dst)
    cv2.imshow('3',edges)
    cv2.imshow('2', img)
    cv2.waitKey(0)  
            
    cv2.destroyAllWindows()


def handleStandardImg(standardImg):
    '''
    这个函数是为了处理标准的图片拿到之后对其进行二值化，模糊，开闭运算，最终返回 开闭运算的值方便之后的函数处理
    standardImg: 标准的外框图片
    return : 获取到的边缘像素点
    ''' 
   
    gray = cv2.cvtColor(standardImg, cv2.COLOR_BGR2GRAY)

    dst = cv2.bilateralFilter(src=gray, d = 5, sigmaColor=150, sigmaSpace = 100)

    # Canny算子求得图像边缘
    edges = cv2.Canny(dst, 70, 150, apertureSize = 3)


    # 闭运算 线膨胀后腐蚀
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)


    # 寻找轮廓
    contours, hier = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # # 获取面积最大的contour
    # cnt = max(contours, key=lambda cnt: cv2.contourArea(cnt))
    cv2.drawContours(standardImg, contours, -1, (0, 0, 255), 1)

    # d = 5
    # sigmaSpace = 10
    # sigmaColor = 200
  
    # # 定义回调函数，此程序无需回调，所以Pass即可
    # def callback(object):
    #     pass
    # # 滑动条
    # cv2.createTrackbar('sigmaColor', 'image', 0, 255, callback)
    # cv2.createTrackbar('d', 'image', 0, 255, callback)
    # cv2.createTrackbar('sigmaSpace', 'image', 0, 255, callback)

    # while(True):
    #     sigmaColor = cv2.getTrackbarPos('sigmaColor', 'image')
    #     sigmaColor = cv2.getTrackbarPos('d', 'image')
    #     sigmaColor = cv2.getTrackbarPos('sigmaSpace', 'image')
    #     dst = cv2.bilateralFilter(src=gray, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaColor)
    #     if cv2.waitKey(10) & 0xFF == ord('q'):
    #         break
    #     cv2.imshow('image', dst)


    # cv2.namedWindow('image',0)
    # cv2.namedWindow('image1',0)
    # cv2.imshow('image', standardImg)
    # cv2.imshow('image1', closing)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return contours 


def getAllFrames(counters, standardData,):
    '''
        获取所有符合标准的矩形并返回
    '''
    AllFrames = standardData['AllFrames']   
    # print(AllFrames)
    AllFramesResult = {}
    for counter in counters:

        M = cv2.moments(counter)
        # ['m00'] 不可以为０否则报错
        if M['m00'] != 0 : 
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            x,y,w,h = cv2.boundingRect(counter)
            thisArea_Rect = w*h
            thisLength_Rect = 2*w + 2*h
            thisArea = cv2.contourArea(counter)
            thisLength = cv2.arcLength(counter,True)

            for frameKey, frameValue in AllFrames.items():
                toleranceArea = evaluateTolerance(thisArea, frameValue['area'])
                toleranceLength = evaluateTolerance(thisLength, frameValue['circumference'])
                
       
                if toleranceArea >= frameValue['tolerance'] and toleranceLength >= frameValue['tolerance']:
                    print(toleranceArea, toleranceLength, frameKey)
                    # 若 AllFramesResult 中有　frameKey　这个值，则还要判断　容差　是否大于已有元素的容差，若没有则加入
                    if frameKey in AllFramesResult.keys() :
                        if AllFramesResult[frameKey][4] <= toleranceArea:
                            AllFramesResult[frameKey] = (x,y,w,h, toleranceLength, toleranceArea)
                    else:    
                        AllFramesResult[frameKey] = (x,y,w,h, toleranceLength, toleranceArea)
                    
    # print(AllFramesResult)
    return AllFramesResult
        

def getStudentNumberImage(standardImg, allFrames, standardData):
    '''
        这个函数是为了获取学号来用的
    '''

    IDFrameData = allFrames['ID']
    IDFrameImage = standardImg[IDFrameData[1]:IDFrameData[1]+IDFrameData[3], IDFrameData[0]:IDFrameData[0]+IDFrameData[2]]

    standardIDFrame = standardData['AllFrames']['ID']
    pane = standardIDFrame['pane']
    paneLeft = standardIDFrame['padding_left']
    paneArea = standardIDFrame['paneArea']
    paneLength = standardIDFrame['paneCircumference']

    gray = cv2.cvtColor(IDFrameImage, cv2.COLOR_BGR2GRAY)

    dst = cv2.bilateralFilter(src=gray, d = 5, sigmaColor=150, sigmaSpace = 100)

    # Canny算子求得图像边缘
    edges = cv2.Canny(dst, 70, 150, apertureSize = 3)


    # 闭运算 线膨胀后腐蚀
    kernel = np.ones((4,4),np.uint8)
    closing = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)

    # 寻找轮廓
    contours, hier = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(IDFrameImage, contours, -1, (2, 255, 255), 1)

    
    studentID= []
    print('StandardArea:-----------------')
    print(paneArea)
    print('StandardArea:-----------------')
    print(paneLength)
    for contour in contours:

        # approx = cv2.approxPolyDP(contour, 0.1 * paneLength, True) 

        x,y,w,h=cv2.boundingRect(contour)

        thisArea = w * h
        thisLength = (w+h) * 2

        toleranceArea = evaluateTolerance(thisArea, paneArea)
        toleranceLength = evaluateTolerance(thisLength, paneLength)
    
        if toleranceArea> 0.7 and toleranceLength > 0.7:
            print(toleranceArea, toleranceLength)
            x,y,w,h = cv2.boundingRect(contour)
            thisNumber = closing[y+4 :y+h-4 ,x+3:x+w-3]
            thisNumber = cv2.resize(thisNumber, (28,28), interpolation=cv2.INTER_LANCZOS4)
            print(thisNumber.shape)
            studentID.append(thisNumber)
            img=cv2.rectangle(IDFrameImage,(x,y),(x+w,y+h),(0,255,0),1)

    print(np.asarray(studentID).shape)
    # for i in range(5):
    #     start = paneLeft + pane[0] * i
    #     end = paneLeft + pane[0]* i + pane[0]

    #     thisNumber = closing[  IDFrame[1]: IDFrame[1] + IDFrame[3] , start:end]
    #     thisNumber = cv2.resize(thisNumber, (28,28), interpolation=cv2.INTER_LANCZOS4)
    #     studentID.append(thisNumber)
        # np.append(studentID, closing[  IDFrame[1]: IDFrame[1] + IDFrame[3] , start:end] , axis=0)

    cv2.imshow('1', studentID[0])
    cv2.imshow('11', studentID[1])
    cv2.imshow('111', studentID[2])
    cv2.imshow('1111', studentID[3])
    cv2.imshow('11111', studentID[4])
    cv2.imshow('111111', studentID[5])
    cv2.imshow('1111', studentID[4])
    cv2.imshow('22', edges)
    cv2.imshow('33', IDFrameImage)

    kerasLoad.loadImg(np.asarray(studentID))

    cv2.waitKey(0)
    cv2.destroyAllWindows()



def huofumanTest(img, studentFrameStandard):
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # 中值滤波 过滤噪声，保留边缘信息
    gray = cv2.medianBlur(gray,5) 
    # Canny算子求得图像边缘
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    
    minLineLength = 15
    maxLineGap = 5

    lines = cv2.HoughLinesP(edges,1,np.pi/180,100, minLineLength,maxLineGap)

    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(img, (x1,y1), (x2,y2),(0, 0 ,255),1)
            cv2. imshow("edges", edges)
            cv2. imshow("lines", img)
    


    # cv2.imshow('2', img)
    cv2.waitKey(0)  
            
    cv2.destroyAllWindows()

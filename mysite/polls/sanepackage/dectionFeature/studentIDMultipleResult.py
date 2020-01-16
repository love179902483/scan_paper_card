
import cv2
import numpy as np

def getMultipleResult(standardImg, standardData, frameResult):
    '''
        三个参数，标准图片，标准的参数数据，上一步得到的所有框子的结果．
    '''
    if "MultipleChose" in frameResult.keys():
        print("MultipleChose in this page! Result is ：") 
        print(frameResult['MultipleChose'])


        MultipleResult = {}
        

        x = frameResult['MultipleChose'][0]
        y = frameResult['MultipleChose'][1]
        w = frameResult['MultipleChose'][2]
        h = frameResult['MultipleChose'][3]

        
        standardMultipleData = standardData['AllFrames']['MultipleChose']
        # 整个选择题的左边距
        padding_left = standardMultipleData["padding_left"]
        # 整个选择题的上边距
        padding_top = standardMultipleData["padding_top"]
        # 每个选项的标准大小
        pane = standardMultipleData["pane"]
        # 选项的标准面积
        paneArea = standardMultipleData["paneArea"]
        # 选项的标准周长
        paneCircumference = standardMultipleData["paneCircumference"]
        # 选项的容差范围(最小，最大)
        paneTolerance = standardMultipleData["paneTolerance"]
    
        # 获取标准的选择题的小框子
        sourceImg = standardImg[y: y+h, x: x+w]
        gray = cv2.cvtColor(sourceImg, cv2.COLOR_BGR2GRAY)
        # 中值滤波
        img_mediaBlur = cv2.medianBlur(gray,3)
        # 获取轮廓
        # img_canny = cv2.Canny(img_mediaBlur, 80,150,apertureSize = 3)
        # 获取二值图像
        _,img_threshold = cv2.threshold(img_mediaBlur, 127, 255, cv2.THRESH_BINARY_INV)

        try: 
            #   获取二值化图像的一部分
            #　规定游标大小
            kernel = np.ones((8,8),np.uint8)
            # 开运算图像
            # 闭运算图像
            img_opening = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, kernel,iterations=1)      
            contours, hierarchy = cv2.findContours(img_opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            print('StandardArea And StandardLength')
            print(paneArea, paneCircumference)

            count = 0
            for contour in contours:
                # 计算本框框面积
                realArea = cv2.contourArea(contour)
                # 计算本框框周长
                realLength = cv2.arcLength(contour,True)
                realToleranceAreaTolerance = round(realArea/paneArea, 2)
                realToleranceLengthTolerance = round(realLength/paneCircumference, 2)



                print('GOT RESULT [REAL]: ')
                print(realArea, realLength)
                print('GOT RESULT　［TOLERANCE］: ')
                print(realToleranceAreaTolerance, realToleranceLengthTolerance) 


                if  paneTolerance[0] <= realToleranceAreaTolerance <= 1.1 and paneTolerance[1] <= realToleranceLengthTolerance <= 1.1:
                    count = count + 1
                    M = cv2.moments(contour)
                    if M['m00'] != 0 :
                        # 得到符合标准的中心点 x ,y 为 cx ,cy
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])

                        cv2.circle(sourceImg,(cx,cy), 2 ,(255, 255, 0), 5)
                        questionNumber = int((cx-padding_left)/pane[0]) + 1
                        # 因为题号也占了一个单位，所以不需要给其+1
                        questionAnswer = int((cy-padding_top)/pane[1]) 
                        print('Question [Answer]: ')
                        print(questionAnswer)
                        # 如果　答案实在第　０行或者第５行则表示是题号行，则跳过
                        if questionAnswer == 0 or questionAnswer == 5: continue

                        if questionAnswer > 5 :
                            questionNumber = questionNumber + 11 
                            questionAnswer = questionAnswer - 5

                        MultipleResult[questionNumber] = questionAnswer

            # print(count)
        except Exception as error :
            print(error)
        finally :
            # 按照题号排序所有题和答案
            MultipleResultSorted = sorted(MultipleResult.items(), key=lambda x: x[0])
            cv2.imshow('11',sourceImg)
            cv2.imshow('111',img_opening)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("得到的选择题结果：")
            print(MultipleResultSorted)
            
            return MultipleResultSorted, sourceImg

    else: 
        return False, False
        print("MultipleChose not in this page!!!")


def getStudentNumber(standardImg, standardData, frameResult):
    '''
        三个参数，标准图片，标准的参数数据，上一步得到的所有框子的结果．
    '''
    if "MultipleChose" in frameResult.keys():
        print("Student Number in this page! Result is ：") 
        print(frameResult['ID'])


        StudentNumber = {}
        

        x = frameResult['ID'][0]
        y = frameResult['ID'][1]
        w = frameResult['ID'][2]
        h = frameResult['ID'][3]

        
        standardStudentNumberData = standardData['AllFrames']['ID']
        # 整个选择题的左边距
        padding_left = standardStudentNumberData["padding_left"]
        # 整个选择题的上边距
        padding_top = standardStudentNumberData["padding_top"]
        # 每个选项的标准大小
        pane = standardStudentNumberData["pane"]
        # 选项的标准面积
        paneArea = standardStudentNumberData["paneArea"]
        # 选项的标准周长
        paneCircumference = standardStudentNumberData["paneCircumference"]
        # 选项的容差范围(最小，最大)
        paneTolerance = standardStudentNumberData["paneTolerance"]
    
        # 获取标准的选择题的小框子
        sourceImg = standardImg[y: y+h, x: x+w]
        gray = cv2.cvtColor(sourceImg, cv2.COLOR_BGR2GRAY)
        # 中值滤波
        img_mediaBlur = cv2.medianBlur(gray,3)
        # 获取轮廓
        # img_canny = cv2.Canny(img_mediaBlur, 80,150,apertureSize = 3)
        # 获取二值图像
        _,img_threshold = cv2.threshold(img_mediaBlur, 127, 255, cv2.THRESH_BINARY_INV)

        try: 
            #   获取二值化图像的一部分
            #　规定游标大小
            kernel = np.ones((8,8),np.uint8)
            # 开运算图像
            # 闭运算图像
            img_opening = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, kernel,iterations=1)      
            contours, hierarchy = cv2.findContours(img_opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            print('StandardArea And StandardLength')
            print(paneArea, paneCircumference)

            count = 0
            for contour in contours:
                # 计算本框框面积
                realArea = cv2.contourArea(contour)
                # 计算本框框周长
                realLength = cv2.arcLength(contour,True)
                realToleranceAreaTolerance = round(realArea/paneArea, 2)
                realToleranceLengthTolerance = round(realLength/paneCircumference, 2)
                print('GOT RESULT [REAL]: ')
                print(realArea, realLength)
                print('GOT RESULT　［TOLERANCE］: ')
                print(realToleranceAreaTolerance, realToleranceLengthTolerance) 
                if  paneTolerance[0] <= realToleranceAreaTolerance <= 1.1 and paneTolerance[1] <= realToleranceLengthTolerance <= 1.1:
                    count = count + 1
                    M = cv2.moments(contour)
                    if M['m00'] != 0 :
                        # 得到符合标准的中心点 x ,y 为 cx ,cy
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])

                        cv2.circle(sourceImg,(cx,cy), 2 ,(255, 255, 0), 5)
                        questionNumber = int((cx-padding_left)/pane[0]) + 1
                        # 因为题号也占了一个单位，所以不需要给其+1
                        questionAnswer = int((cy-padding_top)/pane[1]) 
                        print('Question [Answer]: ')
                        print(questionAnswer)
                        StudentNumber[questionNumber] = questionAnswer
                        # 如果　答案实在第　０行或者第５行则表示是题号行，则跳过

            print(count)
        except Exception as error :
            print(error)
        finally :
            # 按照题号排序所有题和答案
            StudentNumberResultSorted = sorted(StudentNumber.items(), key=lambda x: x[0])
            
            StudentNumber = ""
            cv2.imshow('11',sourceImg)
            cv2.imshow('111',img_opening)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # print("得到的考生号［处理之前］：")
            for numberKey,studentNumber in StudentNumberResultSorted:
                print(numberKey, studentNumber)
                StudentNumber = StudentNumber + str(studentNumber)
            print("得到的考生号［处理之后］：")
            print(StudentNumberResultSorted, StudentNumber)
            

            return StudentNumber, StudentNumberResultSorted, sourceImg

    else: 
        return False, False
        print("Student Number not in this page!!!")
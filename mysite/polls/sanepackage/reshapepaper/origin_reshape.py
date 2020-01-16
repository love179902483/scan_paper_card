import matplotlib.pyplot as plt
import cv2


def upsideDown():
    print(1111)


def reshape(img_path , saneStandard):
    print(img_path)
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.imread('./test111.jpg', cv2.IMREAD_GRAYSCALE)


    print(img_gray.shape)

    ret, thresh1 = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY_INV)

    cnts, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cnts = sorted(cnts,key = cv2.contourArea,reverse=True)

    # 最大形状的图形
    maxcnt = []
    # 最大形状图形下的点
    maxcntPoint = []
    try:

        for cnt in cnts:
            maxperi = 0;
            
            if len(maxcnt)!=0:
                maxperi = cv2.arcLength(cnt,True)


            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            if len(maxcnt) == 0 and len(approx) == 4:
                maxcnt = approx
            elif len(approx) == 4 and maxperi<peri: 
                maxcnt = approx
            else:
                continue

        # 若没有查询到4个定点的图形则会报错
        maxcntPoint = maxcnt[3]     
    except Exception as err:
        print(err)
    finally:
        print(maxcnt)

    # 获取找出的　４个点的正外接矩形
    rectPoint = cv2.boundingRect(maxcnt)
    print('maxcntPoint:')
    print(rectPoint)
    # img_cnts = cv2.drawContours(img, [rectPoint], -1 , (0,255,0),10)
    
    #　画一个框框
    # cv2.rectangle(img, (rectPoint[0],rectPoint[1]),(rectPoint[2],rectPoint[3]), (0,255,255) ,3)

    img_aim = img[0: rectPoint[3], 0: rectPoint[2]]

    sourceImgHeight = rectPoint[3]
    sourceImgWidth = rectPoint[2]

    standardHeight = saneStandard['Paper']['height']
    standardWidth = saneStandard['Paper']['width']

    aimWidth = int((sourceImgWidth/sourceImgHeight) * standardHeight) 

    imStandardShape = cv2.resize(img_aim, (aimWidth,standardHeight), interpolation=cv2.INTER_LANCZOS4)

    # cv2.namedWindow('test',0)
    # cv2.imshow('test',imStandardShape)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return imStandardShape

    # # print(len(cnts))
    # # # print(approx[1][0][1])
    # # # print(approx[3][0])
    # # plt.imshow(img_gray)
    # # plt.imshow(img_gray)
    # # plt.show()
  
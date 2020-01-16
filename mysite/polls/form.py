from django.http import HttpResponse
from django.shortcuts import render
import cv2

import os 

from django.views.decorators.csrf import csrf_exempt

from polls.sanepackage.sanemechine import mysane

from polls.sanepackage.reshapepaper import origin_reshape

from polls.sanepackage.dectionFeature import studentFrames

from polls.sanepackage.dectionFeature import studentIDMultipleResult

import numpy as np


# (2479, 3508)
SaneVariables_big={
    "Paper":{
        "shape": (3508, 2479),
         "outFrame": {
            "width": 2370,
            "height": 3390,
            "circumference": 2*2370 + 3390*2,
            "area": 2370 * 3390,
            "tolerance": 0.8,
        },

        "MultipleChose": {
            "shape": (2340, 330),
            "padding_left": 15,
            "padding_top": 15,
            "pane": (90, 60),
        },
        "ID":{
            "shape": (2340, 90),
            "pane": (90, 90),
            "padding_left": 180,
        }
    }
}


# 2479 ÷ 1240 = 2
# 3508 ÷ 1754 = 2
# 1240×1754
# shape 是(行，列)

SaneVariables_normal={
    "Paper":{
        "shape": (1754 ,1240),
        "width": 1240,
        "height": 1754,
        
        "paperName": "测试考试",
        "paperNumber": 123456,
        "testStudent": 222222,
        "saveDir": 'uploadImage'
    },
    "outFrame": {
        "width": 1185,
        "height": 1695,
        "circumference": 2*1185 + 1695*2,
        "area": 1185 * 1695,
        "tolerance": 0.8,
    },
    # AllFrames 是所有框子，包括习题，包括ＩＤ号
    # 每个框子都需要知道Ｙ轴的中心坐标．
    "AllFrames": {
        "MultipleChose": {
            # "shape": (562, 79), #可能有问题( 561.637, 79.113)
            "width": 1185,
            "height": 165,
            "circumference": 2*1185+165*2,
            "area": 1185 * 165,
            "tolerance": 0.85,

            "padding_left": 13,  
            "padding_top": 13,  
            "pane": (45, 30), 
            "paneArea": 45* 30,
            "paneCircumference": 2*45+30*2,
            # （面积容差，周长容差）　容差:真实面积/标准面积
            "paneTolerance": (0.3, 0.5),
        },
        "ID":{
            # "shape": (562, 22), #可能有问题( 561.637, 21.576)
            "width": 1155,
            "height": 45,
            "centerHeight": (21, 42),
            "circumference": 2*1155+45*2,
            "area": 1155*45,    
            "tolerance": 0.85,

            "ratio": round(1185/45, 2), #长宽的比例
            "pane": (45, 45),   #可能有问题( 561.637, 21.576)
            "paneArea": 45*45,
            "paneCircumference": 45*2 + 45*2,
            "padding_left": 75,#可能有问题( 561.637, 43.152)
        }
    },
    "MultipleChose": {
        "width": 1185,
        "height": 165,
        "circumference": 2*1185 + 165*2,
        "area": 1185 * 165,
        "padding_left": 47,  #可能有问题( 3.6)
        "padding_top": 22,   #可能有问题( 3.6, 3.596)
        "pane": (135, 90),   #可能有问题（21.601, 14.384）
        "tolerance": 0.8,
    },
    "ID":{
        # "shape": (562, 22), #可能有问题( 561.637, 21.576)
        "height": 45,
        "width": 1185,
        "centerHeight": (0, 45),
        "circumference": 2*1185+45*2,
        "area": 1185*45,    
        "ratio": round(1185/45, 2), #长宽的比例
        "pane": (45, 45),   #可能有问题( 561.637, 21.576)
        "padding_left": 90,#可能有问题( 561.637, 43.152)
        "tolerance": 0.8,
    }
}

# 外层框子信息
outFrameWith = 1160
outFrameHeight = 1660
outFramePaddingLeft = 10
outFramePaddingTop = 10

# 选择题框子信息
multipleChoiceFrameWith = 720
multipleChoiceFrameHeight = 420
multipleChoiceFramePaddingLeft = 10
multipleChoiceFramePaddingTop = 10

# 每个涂卡项的信息
paneWith = 40 + 20
paneHeight = 20 + 20

# 学生编号信息
studentNumberFrameWidth = 440
studentNumberFrameHeight = 420
studentNumberFramePaddingTop = 10
studentNumberFramePaddingLeft = 10

# 图框的容差　(面积最小容差，最小周长容差)
StandardPaneTolerance = (0.2, 0.5)

SaneVariables={
    "Paper":{
        "shape": (1754 ,1240),
        "width": 1240,
        "height": 1754,
        
        "paperName": "测试考试",
        "paperNumber": 123456,
        "testStudent": 222222,
        "saveDir": 'uploadImage'
    },
    "outFrame": {
        "width": outFrameWith,
        "height": outFrameHeight,
        "circumference": 2*outFrameWith + outFrameHeight*2,
        "area": outFrameWith * outFrameHeight,
        "tolerance": 0.8,
    },
    # AllFrames 是所有框子，包括习题，包括ＩＤ号
    # 每个框子都需要知道Ｙ轴的中心坐标．
    "AllFrames": {
        "MultipleChose": {
            "width": multipleChoiceFrameWith,
            "height": multipleChoiceFrameHeight,
            "circumference": 2*multipleChoiceFrameWith + multipleChoiceFrameHeight*2,
            "area": multipleChoiceFrameWith * multipleChoiceFrameHeight,
            "tolerance": 0.85,

            "padding_left": outFramePaddingLeft,  
            "padding_top": outFramePaddingTop,  
            "pane": (paneWith, paneHeight), 
            "paneArea": paneWith * paneHeight,
            "paneCircumference": 2*paneWith + paneHeight*2,
            # （面积容差，周长容差）　容差:真实面积/标准面积
            "paneTolerance": StandardPaneTolerance,
        },
        "ID":{
            "width": studentNumberFrameWidth ,
            "height": studentNumberFrameHeight,
            "centerHeight": (21, 42),
            "circumference": 2*studentNumberFrameWidth+studentNumberFrameHeight*2,
            "area": studentNumberFrameWidth*studentNumberFrameHeight,    
            "tolerance": 0.85,

            "pane": (paneWith, paneHeight),
            "ratio": round(studentNumberFrameWidth/studentNumberFrameHeight, 2), #长宽的比例
            "paneWidth": paneWith,
            "paneHeight": paneHeight,
            "paneArea": paneWith * paneHeight,
            "paneCircumference": paneWith*2 + paneHeight*2,
            "padding_left": studentNumberFramePaddingLeft,#可能有问题( 561.637, 43.152)
            "padding_top": studentNumberFramePaddingTop,
            "paneTolerance": StandardPaneTolerance,
        }
    },
}


@csrf_exempt
def testSearch(request):
    request.encoding='utf-8'
    print(request.method)
    if request.method == 'GET' :
        message = request.Get('a', default='100')
        message1 = request.Get('b', default='100')
        # if 'q' in request.GET and request.GET:
        #     message = '你搜索的内容为: ' + request.GET['q']
        #     print
        # else:
        #     message = '你提交了空表单'
    elif request.method == 'POST':
        # 这个是为了去除扫描出来的多余白色区域
        mysane.sane( SaneVariables, 100,mode='Color',multiple=False)
        

        # # 获取到所有纸张和选择题相关信息
        # paperinfo, multipleQustionInfo ,studentIDInfo, outFrame =  studentFrames.getStandardDetails(SaneVariables)

        # # origin_img = origin_reshape.reshape('/home/qinyu/myproject/python_project/examination_pro/mysite/inventory/1569663458.jpg', SaneVariables)

        # # 这个是test，读入一张图片 1569663458.jpg
        # origin_img = cv2.imread('/home/qinyu/myproject/python_project/examination_pro/mysite/inventory/1570616969.jpg')
        # print('This is after shape', origin_img.shape)

        # standardImg = studentFrames.getOutFrame(origin_img, outFrame)

        # counters = studentFrames.handleStandardImg(standardImg)

        # # 返回所有框子的值
        # AllFrames = studentFrames.getAllFrames(counters, SaneVariables)

        # print(AllFrames)
        # for key, thisValue in AllFrames.items():
        #     print(thisValue)
        #     # cv2.rectangle(standardImg, (thisValue[0],thisValue[1]), (thisValue[0]+thisValue[2], thisValue[1]+thisValue[3]), (255, 255, 0), 3)

        # # 目前手写数字识别可能有些问题，主要是数字识别出来不太对，所以改用涂卡的方式．
        # # studentID = studentFrames.getStudentNumberImage(standardImg, AllFrames, SaneVariables)

        # '''
        #     以下为正式解析数据
        # '''

        # # 第一步确定是否为有选择题的第一页纸,

        # # 通过涂卡的形式判断出来是哪个人
        # StudentID, StudentID_array, StudentNumberImg  = studentIDMultipleResult.getStudentNumber(frameResult = AllFrames, standardData = SaneVariables, standardImg = standardImg)

        # # 获取某次考试某个学生的路径，只有在确定是哪个人，也就是拿到某个人的学生编号之后才能确定最后对应学生的图片存储的最终路径
        # StudentSavePath = mysane.getSavePath(StudentID, SaneVariables)

        # # 如果为有选择题的那一页则得出所有选择题的答案,
        # MultipleResult, MultipleImg = studentIDMultipleResult.getMultipleResult(frameResult = AllFrames, standardData = SaneVariables, standardImg = standardImg ) 
        
        # # 存储标准框子以及选择题到学生路径下
        # outFramePath = os.path.join(StudentSavePath, '0.jpg')
        # studentNumberPath = os.path.join(StudentSavePath, '1.jpg')
        # multiplePath = os.path.join(StudentSavePath, '2.jpg')

        # print(outFramePath)
        # print(multiplePath)
        # cv2.imwrite(outFramePath, standardImg)
        # cv2.imwrite(studentNumberPath, StudentNumberImg)
        # cv2.imwrite(multiplePath, MultipleImg)
        


        # # cv2.drawContours(standardImg, counters, -1, (0, 0, 255), 1)

        # # cv2.imshow('111',standardImg)
        # # cv2.waitKey(0)
        # # cv2.destroyAllWindows()

        
        
        # # cv2.imshow('test', outFrame)
        # # cv2.waitKey(0)  
        # # cv2.destroyAllWindows()

        # # studentFrames.getStudentIDPoints(outFrame ,studentIDInfo)
        # # studentFrames.getStudentIDPoints(origin_img, studentIDInfo)

        print(request.POST.get('a'))
        message =  request.POST.get('a')

    return HttpResponse(message)
import pyinsane2
import os
import time
from polls.sanepackage.reshapepaper import origin_reshape

from polls.sanepackage.dectionFeature import studentFrames
import cv2

# 定义最终文件存放的地址
InventoryPath = os.path.join(os.getcwd(), 'inventory', 'temp') 
UploadPath = os.path.join(os.getcwd(), 'inventory', 'uploadImage')
print(InventoryPath)

def getTempPath():
    '''
        返回temp的图片地址
    '''
    return InventoryPath

def getUploadPath():
    '''
        返回上传的图片地址
    '''
    return UploadPath

def createPageDir(aimPath):
    '''
        判断定义的 inventory　文件夹是否存在不存在则创建一个
    '''
    print(aimPath)
    
    if not os.path.exists(aimPath):
        os.makedirs(aimPath)
    
    return aimPath

def createPagePath(dirPath, fileName):
    '''
        生成保存的文件地址
    '''
    finalPath = os.path.join(dirPath, fileName)
    print(finalPath)
    return finalPath


def sane(sanevariables, resolution=100, mode="Color", multiple=False ):

    # 先查看iventory文件夹是否存在
    inventory = createPageDir(InventoryPath)
    

    try:
        pyinsane2.init()
        devices = pyinsane2.get_devices()
        print(devices)
        if len(devices) > 0 :
            device = devices[0]

            print('I am going to use the following scanner: %s' %(str(device)))
            scanner_id = device.name


            try:
                pyinsane2.set_scan_area_pos(device, 'source', ['ADF', 'Feeder'])

            except Exception as e:
                print(e)

        #     pyinsane2.set_scanner_opt(device, 'resolution', [resolution])

        #     pyinsane2.set_scanner_opt(device, 'mode', [mode])

        #     pyinsane2.maximize_scan_area(device)

        #     try :
        #         scan_session = device.scan(multiple=multiple)
        #         print('scanning--------------------')
        #         while True:
        #             try:
        #                 scan_session.scan.read()
        #             except EOFError:
        #                 print("Got page %d" % (len(scan_session.images)))
        #                 img = scan_session.images[-1]
        #                 SaneTime = str(int(time.time()))
        #                 # 以时间戳的形式存储扫描结果为　　"时间戳.jpg"
        #                 SanPathName = createPagePath(inventory, SaneTime+'.jpg')
                        
        #                 # imgpath = os.path.join('test111.jpg')
        #                 img.save(SanPathName)

        #                 # 将扫描出来的多余大片白色区域去掉
        #                 reshapeImg = origin_reshape.reshape(SanPathName, sanevariables)

        #                 # 寻找学号填写的格子，来判断是否是可以解析的扫描结果
        #                 # studentFrames.dectionStudentIDFrame(reshapeImg, )
                        
        #                 # 判断是否是上下颠倒的图片
        #                 # upsideDown = origin_reshape.upsideDown()
        #                 cv2.imwrite(SanPathName, reshapeImg)

        #     except StopIteration:
        #             print("Got %d pages" % len(scan_session.images))

        # else:
        #     print('没有找到打印机')
    except EOFError as err:
        # print(err)
        print('fuck')
    finally:
        print(1111)
        
        # pyinsane2.exit()

def getSavePath(studentID, standardData):
    '''
        通过本次的考试号以及考生的编号，在本地先生成一个存储的文件夹
    '''
    examinationNumber = standardData['Paper']['paperNumber']
    studentImgPath = os.path.join(InventoryPath, standardData['Paper']['saveDir'] ,str(examinationNumber), str(studentID))

    # 先查看iventory文件夹是否存在,不存在则生成
    studentSavePath = createPageDir(studentImgPath)
   
    return studentSavePath

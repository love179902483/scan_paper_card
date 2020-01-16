from flask import Flask, request, url_for, redirect
from config.variable import SaneVariable
from controll import saneControll
import pyinsane2
import cv2
# This is test CLASS
from service.getPerson.getOutFrameService import GetOutFrame
from service.getPerson.getPersonService import GetPersonInfo
from service.getPerson.getThisPaperPage import GetPaperPage
from service.getPerson.reshapePaper import ReshapePaper
from service.getPerson.transferAndCut import TransferAndCut
from service.sane.sanePaperService import SanePaper
from service.sane.prepareSane import PrepareSaneFile
from service.getPerson.getTempPage import TempPage
from service.testRedis import Test
from config.redisConfig import RedisPool

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/a')
def memeda():
    return redirect(url_for('login')) 

@app.route('/b/<userName>')
def hehe(userName):
    return "User is %s" % userName

@app.route('/c/<int:userName>')
def user(userName):
    print(SaneVariable().getMultipleChose())
    return "User is %s" % userName

@app.route('/sane', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return saneControll.mySane()

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        # sanVariable = SaneVariable().getSanVariable()
        # print(sanVariable)
        # setResult = SaneVariable().setToRedis(sanVariable)
        # RedisPool().redisPool().sadd('scannerList', '33456')
        # RedisPool().redisPool().sadd('scannerList', '334561')
        # print(setResult)


        # TempPage().walkTempPage()
        # Test()
        
        

        # testPrepareSaneFile =  PrepareSaneFile()
        # testPrepareSaneFile.createFile()
        # testPrepareSaneFile.getVariableFromBatchFile()
        SanePaper().sanePaper()

        # # 处理所有图片到A4
        # getOutFrame = GetOutFrame(SaneVariable.getPaper(), SaneVariable.getOutFrame())
        # # print(str(SaneVariable().getSanVariable()))
        # print(SaneVariable.getPaper())
        # # pictureList = getOutFrame.allTempPicture

        # # 获取第一张仿射变换后的标准图片 三通道
        # standardImage = getOutFrame.init()

        # standardImageGray = cv2.cvtColor(standardImage, cv2.COLOR_BGR2GRAY)

        # # 处理某一张图片，获取这张图片的页码数
        # getPaperPage = GetPaperPage(standardImageGray, SaneVariable.getPageFoot())
        # thisPageID = getPaperPage.getPage()
        
        # # 根据获取到的ID获取本页的所有变量信息
        # pageData = SaneVariable.getAllPages()['page'+str(thisPageID)]

        # # 根据仿射变换后的图片以及获取的页数获取本页图片的所有信息
        # TransferAndCut

        # print(pageData)

        # for i in pictureList:
        #     thisReshape = ReshapePaper(i, SaneVariable.getSanVariable())
        #     thisReshape.reshape()
            # print(thisReshape.reshapeImage.shape)

        # return str(pictureList.allTempPicture)

        return str(setResult)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    



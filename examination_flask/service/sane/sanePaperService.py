
# -*- coding: utf-8 -*-
from unit import unit

import pyinsane2
import sys
import time
import os
import threading
from config import pathVariable

class SanePaper():
    def __init__(self):
        self.tempPath = pathVariable.PathVariable.getTempPath()
        self.uploadImagePath = pathVariable.PathVariable.getUploadPath()

    def createInventory(self):
        '''
            tempPath  临时文件的存放地址
            uploadImage 图片扫描之后的存放地址
            创建 inventory/temp 和 inventory/uploadImage 文件夹
        '''
        unit.createPageDir(self.tempPath)
        unit.createPageDir(self.uploadImagePath)

        return '成功创建文件夹 '



    def saveImage(self,filePath,image):
        '''
            启动新线程保存图片
        '''
        image.save(filePath)
        print(filePath)
    def sanePaper(self):
        self.createInventory()

        pyinsane2.init()

        try:
            devices = pyinsane2.get_devices()
            print(devices)
            assert(len(devices) > 0)
            device = devices[0]
            pyinsane2.set_scanner_opt(device, 'resolution', [100])
            # pyinsane2.set_scanner_opt(device, 'source', ['ADF', 'Duplex', 'Feeder'])
            print("I'm going to use the following scanner: %s" % (str(device)))
            # print(device.options['Color'])

            # Beware: Some scanners have "Lineart" or "Gray" as default mode
            # better set the mode everytime
            # adfMode = unicode("ADF Duplex", "utf-8")
            # colorMode = unicode("Color", "utf-8")
            # lineMode = unicode("Color", "utf-8")
            # pyinsane2.set_scanner_opt(device, "source", [adfMode])
            pyinsane2.set_scanner_opt(device, "source", ["ADF Duplex"])
            pyinsane2.set_scanner_opt(device, 'mode', ["Color"])
            # pyinsane2.set_scanner_opt(device, 'mode', [lineMode])
            # Beware: by default, some scanners only scan part of the area
            # they could scan.
            
            # pyinsane2.maximize_scan_area(device)

            scan_session = device.scan(multiple=True)


            try:
                while True:
                    try:
                        print('start read!!!')
                        scan_session.scan.read()
                    except EOFError as error:
                        print(error)
                        # print(len(scan_session.images))

                        print("Got a page! (current number of pages read:)" )

                        t = time.time()
                        fileName = str(int(round(t))) + '.jpeg'
                        fileName1 = str(int(round(t)))+ '1' + '.jpeg'

                        filePathTemp = os.path.join(self.tempPath, fileName)

                        # myImages =  scan_session.images
                        hehe =scan_session.images[-1]
                        newThread = threading.Thread(target=self.saveImage,args=(filePathTemp,hehe,))
                        # newThread2 = threading.Thread(target=saveImage,args=(filePath,hehe,))
                        newThread.start()
                        # newThread2.start()
                        # hehe.save(filePath)
                        # print(len(scan_session.images))

            except StopIteration:
                return 'Document feeder is now empty. Got ' + str(len(scan_session.images))+ ' pages' 
    
        finally: 
            pyinsane2.exit()

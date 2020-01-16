# -*- coding: UTF-8 -*-
import pyinsane2
import cv2
import time
import os
import threading
# from  service import sanePaper


myImages = []
def saveImage(filePath,image):
    image.save(filePath)
    print(filePath)

# sanePaper.createInventory()

pyinsane2.init()


try:
    devices = pyinsane2.get_devices()
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
    
    pyinsane2.maximize_scan_area(device)

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

                filePath = os.path.join('./inventory/uploadImage/', fileName)
                filePath1 = os.path.join('./inventory/uploadImage/', fileName1)

                # myImages =  scan_session.images
                hehe =scan_session.images[-1]
                newThread = threading.Thread(target=saveImage,args=(filePath,hehe,))
                # newThread2 = threading.Thread(target=saveImage,args=(filePath,hehe,))
                newThread.start()
                # newThread2.start()
                # hehe.save(filePath)
                # print(len(scan_session.images))
        
      

    except StopIteration:

        print('Document feeder is now empty. Got %d pages' % len(scan_session.images))
        # print('scan_session images 判断是否有值')
        # print(len(scan_session.images))
        # for i in range(0, len(scan_session.images)):
        #     image = scan_session.images(i)
        #     fileName = os.path.join('./inventory/uploadImage/', str(int(round(t * 1000))) )
        #     print(fileName)
        #     cv2.imwrite(fileName,image)
        #     print(len(scan_session.images))
  
finally: 
    #  for i in range(0, len(scan_session.images)):
    #         image = scan_session.images(i)
    #         fileName = os.path.join('./inventory/uploadImage/', str(int(round(t * 1000))) )
    #         print(fileName)
    #         cv2.imwrite(fileName,image) 
    #         print(len(scan_session.images))
    # print("Got pages %d " % len(scan_session.images))
    pyinsane2.exit()
#     try:
# 		while True:
# 			try:
# 				scan_session.scan.read()
# 			except EOFError:
# 				print ("Got a page ! (current number of pages read: %d)" % (len(scan_session.images)))
#     except StopIteration:
# 		print("Document feeder is now empty. Got %d pages" % len(scan_session.images))
# 	for idx in range(0, len(scan_session.images)):
# 		image = scan_session.images[idx]
# finally:
# 	pyinsane2.exit()


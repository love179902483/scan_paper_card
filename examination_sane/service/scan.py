import os
from config import config 

def getScanCmd(mode='Gray', ScanMode='Duplex', resolution='200'):
    '''
        拼接扫描命令
    '''
    scan_cmd = "scanimage --device-name=canondr:libusb:001:005 --mode={} --Size=A4 --ScanMode={} --resolution={} --format=jpeg --batch=%d.jpg --batch-start=1".format(mode, ScanMode, resolution)
    return scan_cmd


def startScan(scan_cmd):
    imageRootPath = config.getImagePath()
    
    os.system(scan_cmd)
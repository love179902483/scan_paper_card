import os

rootPath = "/home/qinyu/myproject/pythonProject/examination_opencv/examination_pro/examination_flask/"

# 获取项目根路径
projectRoot = os.path.join(os.path.abspath(os.path.dirname(__file__)) , '..')

class PathVariable():
    @staticmethod
    def getTempPath():
        '''
            返回temp的图片地址
        '''
        return os.path.join(rootPath, 'inventory', 'utemp')

    @staticmethod
    def getUploadPath():
        '''
            返回Upload的图片地址
        '''
        return os.path.join(projectRoot, 'inventory', 'uploadImage')
    @staticmethod
    def getLoggingPath():
        '''
            返回log的文件夹地址
        '''
        return os.path.join(projectRoot , 'log')

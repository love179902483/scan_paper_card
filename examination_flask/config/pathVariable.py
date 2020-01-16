import os
class PathVariable():
    @staticmethod
    def getTempPath():
        '''
            返回temp的图片地址
        '''
        return os.path.join(os.getcwd(), 'inventory', 'utemp')

    @staticmethod
    def getUploadPath():
        '''
            返回temp的图片地址
        '''
        return os.path.join(os.getcwd(), 'inventory', 'uploadImage')
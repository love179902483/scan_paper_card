import os


# 页面中扫描参数的配置项
MyConfig = [
    {'name': '分辨率：', 'id': 'resolution', 'data': [('150','150dpi'),('200','200dpi'),('300','300dpi'),('400','400dpi'),]},
    {'name': '模式：', 'id': 'mode', 'data': [('Color','彩色'),('Gray','灰度'),('Black','黑白'),]},
    {'name': '扫描方式：', 'id': 'ScanMode', 'data': [('Simplex','单面'),('Duplex','双面'),]},
]

# 获取image的文件夹位置

def getImagePath():
    ImagePath = os.path.join(os.getcwd(), 'image')
    if not os.path.exists(ImagePath):
        os.makedirs(ImagePath)
    return ImagePath
 
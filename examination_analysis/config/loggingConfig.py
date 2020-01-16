import logging
from config.pathVariable import PathVariable
from myutil import util
import os 


# 判断log文件是否存在，若不存在测创建
util.createPageDir(PathVariable().getLoggingPath())
# 拼接log文件
loggingPath = os.path.join(PathVariable().getLoggingPath(), 'access.log')
print(loggingPath)

logging.basicConfig(filename=loggingPath, format='%(levelname)s %(asctime)s :%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
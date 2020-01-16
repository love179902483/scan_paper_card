from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from config import config
from myutil import getHostIP
from myutil import getNowTime
from service import scan as myscan

app = Flask(__name__)

@app.route('/scan', methods=['GET', 'POST'])
def helloPage():
    '''
        返回静态页面
        以及接收扫描方法
    '''
    if request.method == 'GET':
        return render_template('hello.html', data=[config.MyConfig, getHostIP.get_host_ip()])
    else: 
        print(getNowTime.getNowTime())
        scanCMD = myscan.getScanCmd()
        # myscan.startScan(scanCMD)
        return scanCMD







if __name__ == '__main__':
    app.run(debug=True)
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime
import logging


def func():
    # print(datetime.datetime.now())
    print('hehe')
    logging.warning('this is logging!!!!')
    logging.info('test!!!!!!!!!!!')
    # logging.info('this is info!!!')

def doJob():
    scheduler = BlockingScheduler()
    scheduler.add_job(func, 'interval', seconds=2, id='test_01')
    scheduler.start()


logging.basicConfig(filename='test.log',format='%(asctime)s %(filename)s %(module)s %(funcName)s %(message)s',datefmt='%Y-%m-%d-%H:%M:%S')

doJob()
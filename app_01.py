#7月25日火曜日
#pyw/thre01.pyを使ってスレッドを使って並列処理するプログラム
#地図を動かしながスレッドの生成終了を平行に行うプログラム

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template 
import datetime

import pyw.math13
import pyw.thre01
import cv2
import sys
import time
import numpy as np
from multiprocessing import Pool
from collections import Counter

cap = cv2.VideoCapture('/home/owner/NORM2853.AVI')
if cap.isOpened() == False:
    print('OpenError')
    sys.exit()



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('connection opened...')
        self.my_schedule_func()       # ここで最初に送信を呼び出すと，あとはタイマで自動再送信になる
        
    def on_message(self, message):
        print('received:', message)
        
    def on_close(self):
        print('connection closed...')
 
    def my_schedule_func(self):#随時位置変更
        print("scheduled event fired")
        
        self.write_message("36.4853, 136.5713") # とりあえず固定値を繰り返し送信
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.5), self.my_schedule_func)


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler)
],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static"),
)

if __name__ == "__main__":
    application.listen(8000)
    th_cl = pyw.thre01.TestThread(5, 5)
    th_cl.start()#スレッドスタート
    time.sleep(1)
    tornado.ioloop.IOLoop.instance().start()


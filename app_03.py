#7月26日水曜日
#pyw/thre01.pyを使ってスレッドを使って並列処理するプログラム
#地図の表示をサブスレッドで行うプログラム
#動画の処理をするコードを追加

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template 
import datetime

import threading
import pyw.math13
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


class TestThread(threading.Thread):
    
    def _init_(self):
        threading.Thread.__init__(self)

    def run(self):
        tornado.ioloop.IOLoop.instance().start()

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
    time.sleep(1)
    th_c = TestThread()
    th_c.start()
    time.sleep(1)
#########動画処理############
    while(True):
        ret, frame = cap.read()
        if ret==False:
            break
        cv2.imshow('demo',frame)# frame = frame[960:990, 104:2000]#数字群を表示
        num = [21,22,23,24,25,26,27,28,29,31,32,33,34,36,37,38,39]#19 43 スペースのところ14,17,20,25,35,40#21~29,30~38が
        if cv2.waitKey(1) & 0xFF == ord('q'):#終了
            break
        sampleList = [(i, frame) for i in num]
        py = pyw.math13.math13()
        output = py.multi_pro(sampleList, num)
        print('経度{}'.format(output))
        time.sleep(1.0/30)

cap.release()
cv2.destroyAllWindows()
for i in range (1,5):
    cv2.waitKey(1)


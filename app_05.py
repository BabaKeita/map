#7月27日木曜日
#pyw/thre01.pyを使ってスレッドを使って並列処理するプログラム
#地図の表示をサブスレッドで行うプログラム
#動画の処理をするコードを追加
#my_schedule_func関数でoutputを取得できるようにする
#value関数を作成し返し値で経度緯度を出すようにする
#現在位置に動画を表示させる
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

def value(n):#outputの数値を
    val = 0

    if(n == 1):
        for i in reversed(range(0,8)):#変数num
            if(i <= 3):
               val += output[i] * (10**(3-i))
            elif(i <= 7):
                val += output[i] * (0.1**(i-3))
    elif(n == 2):
        for i in reversed(range(8,16)):
            if(i <= 11):
                val += output[i] * (10**(11-i))
            elif(i <= 15):
                val += output[i] * (0.1**(i-11))
    else:
        print('ERROR')

    return val

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
        #print(output)
        #print(value(1), value(2))
        self.write_message('{0}, {1}'.format(value(1), value(2))) # とりあえず固定値を繰り返し送信
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
##########動画処理#############
    while(True):
        ret, frame = cap.read()
        if ret==False:
            break
        cv2.imshow('demo',frame)# frame = frame[960:990, 104:2000]#数字群を表示
        num = [21,22,23,24,26,27,28,29,31,32,33,34,36,37,38,39]#19 43 スペースのところ14,17,20,25,35,40#21~29,30~38が
        if cv2.waitKey(1) & 0xFF == ord('q'):#終了
            break
        sampleList = [(i, frame) for i in num]
        py = pyw.math13.math13()
        global output
        output = py.multi_pro(sampleList, num)
        print('経度{}'.format(output))
        time.sleep(1.0/30)

cap.release()
cv2.destroyAllWindows()
for i in range (1,5):
    cv2.waitKey(1)


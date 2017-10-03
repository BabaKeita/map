#usr/work/math #7月19日水曜日更新日
#動画の下にある数値部分のみ抜き出し出力 tryming01
#それに二値化処理を行い binary01
#表示されている数値(複数)を正しく認識することができているか確かめる
#それぞれどちらも0と0もしくは255と255の場合の数から判断する
#並列処理を用いて速度アップをしてる。（経度緯度表示）
#参照dataディレクトリの位置を一つ上にしたプログラム
#classを参照してmain.pyからを動かすことで動作するかの検証

import cv2
import sys
import time
import numpy as np
from multiprocessing import Pool
from collections import Counter


#cap = cv2.VideoCapture('http://zeus.info.kanazawa-it.ac.jp/~takago/movie/optflow.flv')
# cap = cv2.VideoCapture('http://www.sharp.co.jp/galileo/guide/movie/sample/sample2_c.mpg') # 学内からは無理かも


cv2.namedWindow("demo", cv2.WINDOW_NORMAL)
ndarr1 = np.loadtxt('/home/owner/work/data/pat.csv', delimiter=',')#ロード

def wrapper(args):#並列処理
    return math13.function(*args)

class math13:
    def function(n, frame):#切り出し2値化一致部分の計算をする関数
        a=int(1+n/10)
        frame = frame[960:990, 104+38*(n-1)+a:104+38*(n-1)+a+29]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#グレイスケール
        retval, frame = cv2.threshold(frame, 200, 255,  cv2.THRESH_BINARY)
        #    cv2.imshow('demo',frame)
        ndarr2 = [flatten for inner in frame for flatten in inner]#2次元配列を1次元配列にする
        L=0
        LL=0
        for j in range(len(ndarr1[0])):
            for k in range(len(ndarr1)):#jが0から9,kが0から869
                if ndarr2[k] == 255:#画像
                    ndarr2[k] = 1 
                L += ndarr1[k][j] * ndarr2[k]
                if ndarr1[k][j] == 0 and ndarr2[k] == 0:
                    L += 1
            if L > LL:#print("if文L{0}>LL{1}数字は{2}。".format(L,LL,m))
                output = j
                LL = L
            L = 0
        return output

    def multi_pro(self,sampleList, num):#並列処理
        p = Pool(len(num))#numの数だけプロセスを作成
        output = p.map(wrapper, sampleList)
        p.close()#開放
        return output

        


import threading
import time
import datetime


class TestThread(threading.Thread):

    """docstring for TestThread"""

    def __init__(self, n, t):
        super(TestThread, self).__init__()
        self.n = n
        self.t = t

    def run(self):
        print(" === start sub thread (sub class) === ")
        for i in range(self.n):
            time.sleep(self.t)
            print("sub thread (sub class) : " + str(datetime.datetime.today()))
        print(" === end sub thread (sub class) === ")

def hoge(n, t):
    print(" === start sub thread (method) === ")
    for i in range(n):
        time.sleep(t)
        print("[%s] sub thread (method) : " % threading.currentThread().getName() + str(datetime.datetime.today()))
    print(" === end sub thread (method) === ")


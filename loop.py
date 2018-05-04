# -*- coding: utf8 -*-
import time                          ## time 시간관련 라이브러리
import threading                     ## 쓰레딩 라이브러리 
import multiprocessing               ## 멀티프로세싱 라이브러리

def yes(no):
    while True:
        print "yes - %d\n" % no
        time.sleep(0.5)              ## 0.5 쉰다.

def no(no):
    while True:
        print "no - %d\n" % no
        time.sleep(0.5)

# t1 = threading.Thread(target = yes, args=(1,))     ## threading.thread 의 의미는 threading 라이브러리 안에 thread라는 함수를 실행 하겠다는 의미.
# t2 = threading.Thread(target = yes, args=(2,))     ## args는 인자 확인

# t1.start()     ## 실행하라.
# t2.start()

# import 로 불러와서 사용하면 이프로그램이 메인이 아니기 때문에 아래 메인으로 만들어주는 구절을 붙임
if __name__ == '__main__':    ## 파이선으로 loop.py을 실행하겠다 했을 때 나는 독립 실행이다라고 인식하게됨 
                              ## __name__이 내가 독립적인 실행인지 import로 불러와서 실행되는건지 확인하기 위해 사용됨
    p1 = multiprocessing.Process(target = yes, args=(1,))  ## 파이선은 컴파일이 없기 때문에 이게 import로 불러와서 실행되는지 main에서 실행되지는 구분을 못함
    p2 = multiprocessing.Process(target = yes, args=(2,))
    p1.start()
    p2.start()

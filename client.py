# -*- coding: utf8 -*-
#소켓 라이브러리 로딩
import socket                       ## socket - 통신을 처리하기 위해 필요한 라이브러리 
# 접속 서버 정보
info = ("127.0.0.1", 9999)          
# TCP 소켓 생성
s = socket.socket()
# 서버 접속
s.connect(info)                     ## 127.0.0.1의 9999번으로 접속
# 데이터 전송
s.send("hello server\n")
# 데이터 수신 및 출력
print s.recv(1024)                  
#접속 종료
s.close()

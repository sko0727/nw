# -*- coding: utf8 -*-
#소켓 라이브러리 로딩
import socket
# 서버 정보
info = ("127.0.0.1", 9999)
# 소켓 생성
s = socket.socket()
# 9999번 포트 바인딩                    # ip(비유: 바닷가 만)로 치면 port(비유: 항구)이고 바인딩을 한다는건 항구를 연다는 것 클라이언트(사용자)가 접속 가능
s.bind(info)
# 바인딩 포트 리스닝                    # listen을 비유하자면 고속도로에 톨게이트같은 느낌 들어오고(송신) 나오고를(수신)을 지켜본다는 의미 
s.listen(5)                            # s.listen(5) listen(5)는 한번에 5개의 접속을 확인하겠다는 의미
# 접속요청 승인
while True:                                     # while 문으로 인해 서버가 계속 실행된다.
    client, address = s.accept()                # 필요한 접속인지 아닌지 확인
    print "[+] new connection from %s(%d)" % (address[0], address[1]) 
    while True:                                 
        try:                       
            # 클라이언트가 전송한 데이터 수신
            data = client.recv(1024)   ## while 문이 한번 실행다되고나면 이 지점으로 돌아와서 대기(다른 접속이 들어와도 들어온 접속이 종료되기 전까지 기다려야함)
        except:                        ## 예외 처리를 위해 만들어진 구문
            print "Exception!!"
            break
        if not data:                   ## 데이터(위의 data 변수)가 없을 때 client.close()를 실행하러 가라.(예외 처리를 위해 만든 구문)
            # 데이터를 보내지 안은 클라이언트 연결 종료
            client.close()
            break
        # 수신 데이터를 클라이언트에 전송
        print "address: %s send data: %s" % \
            (address[0], data)
        # 수신한 데이터를 클라이언트에 전송
        client.send(data)
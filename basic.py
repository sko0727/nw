# -*- coding: utf8 -*-
# 하이
print "hello python" 

# 변수 선언
msg = "hello python"
print msg
# 문자열 슬라이싱
print msg[1:3]
print msg[-3:]
print msg[:-2]
print msg[::-1]

# 리스트
data = []
# 리스트 자료 입력
data.append("hi")
data.append(123)
data.append(1.2)
# 리스트 출력
print data
# 리스트 데이터 제거
data.pop()
print data
data.pop()
print data
#리스트 요소 인덱스 검색
print data.index("hi")
# index 메소드 실패 시 에러 발생
# print data.index("hi2222")

# 사전(딕셔너리)
# { 키 : 값 }
user = {}
user['me'] = {'age': 30, 'address': 'daejoen'}
user['you'] = {'age': 25, 'address': 'seoul'}
# 사전 출력
print user
# 사전 데이터 검색 키 활용
print user['me']
print "user keys:", user.keys()
print "me" in user.keys()

# 제어
# if, if else, if elif else
num = 39.5
if num > 0:
    print "num > 0"

if num > 5:
    print "num > 5"
else:
    print "num < 5"

if num % 2 == 0:
    print "even"
elif num % 2 == 1:
    print "odd"
else:
    print "????"

# 함수
def addition(numbers):       ### def로 함수를 만듬 
    result = 0               ### 함수 안의 값은 함수 안(스코프)에서만 살아있음(?)   
    for number in numbers:
        result += number
    return result

data = [1,2,3]
print addition(data)

def help():
    print "id ------ print user id"
    print "pwd ------ print current path"
    print "quit ------ exit program"
    print "ip ------ print ip address"

help()

# 라이브러리 불러오기
import os
import platform
import subprocess  

# 무한루프
def shell():                                        ## 함수에 아래 기능을 포함 시켰기 때문에 사용할라면 함수 호출               
    while True:
        cmd = raw_input('>>>')
        if cmd == 'id':                             ## if문 안에 아무 값도 없으면 에러가 나기 때문에 pass으로 넘겨버린다(보통 완성되지 않은 기능 부분을 넘길때 사용)
            if platform.system() == 'Windows':
                print os.environ.get('USERNAME')
            else:
                print os.getenv('USER')                        
        elif cmd == 'pwd':
            print os.getcwd()
        elif cmd == 'quit':
            print "bye!!"
            break           
        elif cmd == 'ip':
            if platform.system() == 'Windows':
                buf = subprocess.check_output('ipconfig')
                index = buf.find("IPv4")                        ## IPv4 시작 위치를 찾아서 index에 넣음 .find는 일반적으로 제일 먼저 나오는 부분을 찾아줌.
                newline = buf[index:].find("\n")                ## 위에 찾은 위치부터 다음줄로 갈려면 몇칸이나 가야되나 찾아서 변수에 저장
                # print index, newline
                ipline = buf[index:index+newline]               ## [시작위치:끝지점] ==> 시작위치부터 끝지점 부분까지 읽는다.
                ip = ipline.split(':')                          ## split 은 들어간 값  ':' 기준으로 문자열을 좌 우로 잘름                       
                print ip[1].strip()                             ## strip은 공백이 있는 부분을 날림
            else:
                buf = subprocess.check_output('ifconfig')
                target = 'addr:'
                index = buf.find(target) + len(target)          ## addr 시작 점을 찾음, len 부분으로 target(addr:) <== addr: 부분만큼 건너뜀
                space = buf[index:].find(' ')                   ## ' ' 안에 한 칸 띄어서 한 칸 띄어진 부분을 찾음.
                # print index, space
                print buf[index:index+space]
        
        else:
            help()

# urllib2 사용
import urllib2                                                                  ## 홈페이지를 가져오긴 하지만 화면에 출력 하진 않음
import re                                                                       ## 패턴을 검색할때 사용하는 모듈
url = 'https://box.cdpython.com/ezen/'                
req = urllib2.Request(url)                                                      ## 리퀘스트 urllib2으로 url(위의 변수)을 요청함
res = urllib2.urlopen(req)                                                      ## urlopen url을 염
html = res.read()
# print html
# re 모듈(정규표현식)을 사용한 패턴 매칭                                            
ipaddress, port =  re.findall(r"\d+\.\d+\.\d+\.\d+\/\d+", html)[0].split('/')   ## refindall(r"\d+\.\d+\.\d+\.\d+\/\d+") 앞에 r을 붙이는걸 권장 패턴식    
## *정규표현식* ex) ip 처럼 ***.*.*.* 같은 일정한 패턴을 가지는 것
## split '/'을 기준으로 쪼개고 앞에꺼는 ip 뒤에꺼는 port에 저장가능(파이썬에서만 가능한 문법)
print "ip:", ipaddress, "port:", port
# -*- coding: utf8 -*-
from flask import Flask, render_template, request        ## import 플라스크만 하면 플라스크 안에 모든 함수를 로딩(사용하지 않을 함수로 로딩하게됨)
import hashlib
                                                         ## render_template = html을 포함한다는 의미
app = Flask(__name__)                                    ## from은 라이브러리에서 flask(함수) 하나만 불러오겠다는 의미    
users = {}                                                
                                                         ## (__name__)은 app.py 위 파일 이름과 같은 의미 
@app.route("/")                                          ## @가 붙으면 app.route가 먼저 호출되고 "/"(주소)에 사용자가 접근하면 hello 라는 함수를 호출.
def hello():                                             ## 주소는 cmd에 웹서버 켜놓은 거(flask)에 나와있음.
    return render_template("login.html")      

@app.route("/name")                                      ## 주소 뒤에 name을 붙이고(/name) 사용자가 접근하면 아래 name 함수를 호출, app.route
def name():
    return "ohohoh"

@app.route("/login", methods=['POST'])
def login():
    id = request.form['id']                         
    pw = request.form['pw']
    if id in users:
        if users[id] == hashlib.sha1(pw).hexdigest():
            return "login ok"
        else: 
            return "login fail"
    else:
        return "login fail"
       
@app.route("/join", methods=['GET', 'POST'])             ## url의 정보 전달 방식 get 방식 post 방식 두가지가 있음 get은 주소창 쓰는 그대로 post는 데이터를 전송할수 있음
def join():                                              ## 주소(/join) 으로 접속하면 get이 나오고 주소(/)로 들어가 값을 입력하면 post가 나옴
    if request.method == 'POST':                         ## post 데이터를 보내는 애
        id = request.form['id']                          ## request는 클라이언트가 나에게 보내는 요청에 대한 처리를 함
        pw = request.form['pw']                          ## (.form)전송된 데이터중에 form 형태를 가진 데이터를 내가 가져가서 처리하겠다
        if id not in users:                              ## users 딕셔너리 안에 id가 없을 경우 저장하라
            users[id] = hashlib.sha1(pw).hexdigest()     
        else: 
            return "duplicate!!"
        # return "id: %s, pw: %s" % (id, pw)
        return "join ok"
    return render_template("join.html")                  ## /join으로 주소를 치고 들어왔을 때

@app.route("/add")                              ## 예외 처리 사용자가(예 - /add)만 치고 인자를 하나나 하나도 전달 하지 않았을때 아래 if문을 실행 시켜줌.
@app.route("/add/<int:num1>")
@app.route("/add/<int:num1>/<int:num2>")        ## 함수의 인자를 /(주소)를 통해  전달 할수 있음
def add(num1=None, num2=None):
    if num1 is None or num2 is None:
        return "/add/num1/num2"               
    return str(num1 + num2)                     ## flask는 문자열로 출력하기 때문에 num1과 num2는 숫자형이므로 str로 문자열으로 변경해줘야함 

@app.route("/sub/<int:num1>/<int:num2>")
def sub(num1, num2):
    return str(num1 - num2)       

@app.route("/mul/<int:num1>/<int:num2>")
def mul(num1, num2):
    return str(num1 * num2)

@app.route("/nanum")
@app.route("/nanum/<int:num1>")
@app.route("/nanum/<int:num1>/<int:num2>")
def nanum(num1=None, num2=None):
   if num1 is None or num2 is None:
        return "/nanum/num1/num2"
   elif num1 == 0 or num2 == 0:
        return "0 is not"
   else:
        return str(num1 / num2)

                  
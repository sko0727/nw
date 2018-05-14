# -*- coding: utf8 -*-
from flask import Flask, render_template, request, g, redirect, session, escape     ## import 플라스크만 하면 플라스크 안에 모든 함수를 로딩(사용하지 않을 함수로 로딩하게됨)
import hashlib                                                                      ## g는 플라스크가 실행되는 시점에서 g에게 접근 할수 있다(전역 변수 객체)
import sqlite3                                                                      ## render_template = html을 포함한다는 의미

DATABASE = 'database.db'
                                                         
app = Flask(__name__)                                    ## from은 라이브러리에서 flask(함수) 하나만 불러오겠다는 의미 
app.secret_key = b'_snafklnqkls123m1kmkasd'              ## 세션 만들때 암호화하는 부분   

def get_db():                                            ## get_db라는 함수는 ~(다 못적음)
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)    
    return db                                            ## db라는 변수를 리턴

@app.teardown_appcontext                                 ## 이 구문이 플라스크가 종료될시에 호출한다는 의미
def close_connection(exception):                         ## db 플라스크 앱이 종료될때 기존에 db 커넥션을 종료
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False, modify=False):   ## query를 연결된 데이터베이스에 보내고 가져오는것을 수행하는 함수
    cur = get_db().execute(query, args)
    if modify:                                           ## modify insert일때는 ~(다 못적음)
        try:                                             ## 예외 처리
            get_db().commit()
            cur.close()
        except:
            return False
        return True
    rv = cur.fetchall()                                  ## 커서에 있는 데이터를 몽땅 가져옴 rv(row value)
    cur.close()
    return (rv[0] if rv else None) if one else rv        ## rv[0] = rv에 첫번째 값, if one else rv
                                            
                                                         ## (__name__)은 app.py 위 파일 이름과 같은 의미 
@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/login')

@app.route("/")                                          ## @가 붙으면 app.route가 먼저 호출되고 "/"(주소)에 사용자가 접근하면 hello 라는 함수를 호출.
def hello():                                             ## 주소는 cmd에 웹서버 켜놓은 거(flask)에 나와있음.
    if 'id' in session:                                  ## id라는 값이 세션에 있으면 
        return u'로그인 되었습니다 %s <a href = "/logout">logout</a>'  % escape(session['id'])  ## 앞에 u를 붙이면 한글 출력가능.
    return render_template("login.html")      

@app.route("/name")                                      ## 주소 뒤에 name을 붙이고(/name) 사용자가 접근하면 아래 name 함수를 호출, app.route
def name():
    return "ohohoh"

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        id = request.form['id'].strip()                         
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()
        sql = "select * from user where id='%s' and password='%s' " % (id, pw)
        if query_db(sql, one=True):                   
            ## 로그인이 성공했을때
            session['id'] = id
            return redirect("/")
        else:                                          
            ## 로그인이 실패했을때
            return "<script>alert('login fail');history.bakc(-1);</script>"

    if 'id' in session:     ## id 값이 세션에 있으면
        return redirect("/")

    return render_template("login.html")
       
@app.route("/join", methods=['GET', 'POST'])                         ## url의 정보 전달 방식 get 방식 post 방식 두가지가 있음 get은 주소창 쓰는 그대로 post는 데이터를 가려서 전송할수 있음
def join():                                                          ## 주소(/join) 으로 접속하면 get이 나오고 주소(/)로 들어가 값을 입력하면 post가 나옴
    if request.method == 'POST':                                     ## post 데이터를 보내는 애
        id = request.form["id"].strip()                              ## request는 클라이언트가 나에게 보내는 요청에 대한 처리를 함
        pw = hashlib.sha1(request.form["pw"].strip()).hexdigest()    ## (.form)전송된 데이터중에 form 형태를 가진 데이터를 내가 가져가서 처리하겠다
        
        sql = "select * from user where id='%s'" %id                 ## id가 이미 데이터베이스에있는가 라는 구문
        if query_db(sql, one=True):                                  ## query - one이 트루이면 위에 리턴 rv[0]이 있으면 이미 중복됐다.(?) -다시 보면서 공부
            return "<script>alert('join fail');history.back(-1);</script>"  

        sql = "insert into user(id,password) values('%s', '%s')" % (id, pw)
        print sql
        query_db(sql, modify=True)
        # if id not in users:                                        ## users 딕셔너리 안에 id가 없을 경우 저장하라
        #     users[id] = hashlib.sha1(pw).hexdigest()     
        # else: 
        #    return "duplicate!!"
        # return "id: %s, pw: %s" % (id, pw)
        
        return redirect("/login")                        ## login 페이지로 보낸다.
    
    if 'id' in session:    ## id 값이 세션에 있으면
        return redirect("/")

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

                  
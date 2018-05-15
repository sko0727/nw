# -*- coding: utf8 -*-                                                              ## from은 라이브러리에서 flask(함수) 하나만 불러오겠다는 의미 from flask import 플라스크 안에 라이브러리를 불러오겠다는 의미.
from flask import Flask, render_template, request, g, redirect, session, escape     ## import 플라스크만 하면 플라스크 안에 모든 함수를 로딩(사용하지 않을 함수로 로딩하게됨)
import hashlib                                                                      ## g는 플라스크가 실행되는 시점에서 g에게 접근 할수 있다(전역 변수 객체), 이 코디에서는 데이터 베이스 연결할 때 g에 연결 해서 사용
import sqlite3                                                                      ## render_template - html을 포함한다는 의미, html 파일을 해석해서 변경될 게 있으면 맵핑을 만들어 응답을 줌.
                                                                                    ## hashlib - a라는 값이 들어가면 똑같이 a라는 값을 출력(뭔가를 비교할 때 사용하기 편함, 무결성을 검증 할 때도 사용) 
                                                                                    ## sqlite3 - 데이터베이스 기능을 사용하기 위해 불름
                                                                                    ## request - 많은 기능중 사용한 기능은 어떤 데이터를 보냈는지 처리해주는 객체로 사용
DATABASE = 'database.db'                                                            ## 세션을 사용하지 않으면 로그인 상태를 유지 할수 없다. 서버가 세션이라는 데이터(사용자의 정보)를 보유해서 이 정보를 바탕으로 로그인했는지 안했는지 판단. 
                                                                                    ## escape - 비정상적인 값(예 - id에 코드)을 넣었을 때 이상현상이 일어나지 않도록 예방할때 사용한다고함.
app = Flask(__name__)                                    ## flask를 초기화 하는 부분
app.secret_key = b'_snafklnqkls123m1kmkasd'              ## 세션 만들때 이키를 바탕으로 암호화함.   
                
def get_db():                                            ## get_db라는 데이터베이스를 가져오는 부분
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)     ## sqlite3에 데이터베이스에 접속하는 기능을 이용해 connect(접속)을 맺고 g._datebase에 저장을하고 알기 쉽게 db 변수에 또 저장
    return db                                            ## db라는 변수를 리턴

@app.teardown_appcontext                                 ## 이 구문이 플라스크가 종료될시에 호출한다는 의미
def close_connection(exception):                         ## db 플라스크 앱이 종료될때 기존에 db 커넥션을 종료
    db = getattr(g, '_database', None)                   
    if db is not None:
        db.close()


def query_db(query, args=(), one=False, modify=False):   ## query는 실제 연결된 데이터베이스에 데이터를 보내고 가져오는것을 수행하는 함수, query_db는 select만 처리함(데이터를 변경하지 않기 떄문에 commit은 하지 않음)
    cur = get_db().execute(query, args)                  ## get_db(데이터베이스 커넥션을 가져옴), execute로 query를 보냄 보낸 결과물이 돌아옴
    if modify:                                           ## modify 내가 데이터를 수정하고 싶을때 query를 보낸다음에 commit하고 닫음
        try:                                             ## 예외 처리
            get_db().commit()                            
            cur.close()                                  ## cur 닫음
        except:
            return False                                 ## 위 과정이 이상이 있으면 False
        return True                                      ## 위 과정이 정상이면 True
    rv = cur.fetchall()                                  ## cur에 있는 데이터를 몽땅 가져옴(fetchall), rv는 (row value) 
    cur.close()
    return (rv[0] if rv else None) if one else rv        ## rv[0] = rv에 첫번째 값, if one else rv, one일경우 데이터를 하나만 가져오고, 그외의 경우에는 전체를 가져온다 두경우를 구분하기 위해 만듬.
                                                         ## if one 이 거짓이면 rv 리턴 if one이 트루 이면 (rv[0] if rv else None)부분으로 이동 if rv가 있으면 rv[0]리턴 아무것도 없으면 None을 리턴.
                                                         ## 처리해야 할 데이터가 많으면 많을수록 데이터베이스에 접속하는 시간이 길어져 느려지기 떄문에 위에 구분처럼 필요한 부분을 가져올 필요가 있음.
                                                         ## (__name__)은 app.py 위 파일 이름과 같은 의미 
@app.route('/logout')                     
def logout():
    session.pop('id', None)                              ## 세션에 'id' 정보를 pop(빼다)
    return redirect('/login')                            ## redirect - 돌려보내는 역할, 로그인페이지로 돌려보냄.

@app.route("/")                                          ## @가 붙으면 app.route가 먼저 호출되고 "/"(인덱스)에 사용자가 접근하면 hello 라는 함수를 호출.
def hello():                                             ## 주소는 cmd에 웹서버 켜놓은 거(flask)에 나와있음.
    if 'id' in session:                                  ## id라는 값이 세션에 있으면 로그인 된걸로 간주하겠다는 if문
        return u'로그인 되었습니다 %s <a href = "/logout">logout</a>'  % escape(session['id'])  ## 앞에 u를 붙이면 한글 출력가능. 
    return render_template("login.html")                 ## 들어가지 못했으면 로그인 페이지로 리턴

@app.route("/name")                                      ## 주소 뒤에 name을 붙이고(/name) 사용자가 접근하면 아래 name 함수를 호출, app.route
def name():
    return "ohohoh"

@app.route("/login", methods=['POST', 'GET'])           
def login():
    if request.method == 'POST':          
        id = request.form['id'].strip()                                         ## 전송한 form에서 id라는 찾아서 값을 id에 저장                      
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()               ## 다이제스트 - 메세지 축약, form에서 pw를 찾아 암호화해 pw에 저장
        sql = "select * from user where id='%s' and password='%s' " % (id, pw)  ## 해당하는 아이디와 비밀번호가 데이터베이스에 있는 아이디, 비밀번호인지 확인
        if query_db(sql, one=True):                                             ## query가 정상적으로 동작했다는것은 if문이 트루가됨
            ## 로그인이 성공했을때
            session['id'] = id
            return redirect("/")
        else:                                    
            ## 로그인이 실패했을때
            return "<script>alert('login fail');history.back(-1);</script>"     ## histoty.back 뒤로 보냄

    if 'id' in session:        ## id 값이 세션에 이미 있으면(로그인이 되어있으면)
        return redirect("/")   ## 로그인이 되어있기 때문에 인덱스(/) 페이지로 돌려보냄

    return render_template("login.html")  ## 없다면 로그인 페이지로 리턴
       
@app.route("/join", methods=['GET', 'POST'])                         ## url의 정보 전달 방식 get 방식 post 방식 두가지가 있음 get은 주소창 쓰는 그대로 post는 데이터를 가려서 전송할수 있음
def join():                                                          ## 주소(/join) 으로 접속하면 get이 나오고 주소(/)로 들어가 값을 입력하면 post가 나옴
    if request.method == 'POST':                                     ## post 데이터를 보내는 애
        id = request.form["id"].strip()                              ## request는 클라이언트가 나에게 보내는 요청에 대한 처리를 함
        pw = hashlib.sha1(request.form["pw"].strip()).hexdigest()    ## (.form)전송된 데이터중에 form 형태를 가진 데이터를 내가 가져가서 처리하겠다
        
        sql = "select * from user where id='%s'" %id                 ## id가 이미 데이터베이스에있는가 라는 것을 검증하기 위한 구문
        if query_db(sql, one=True):                                  ## query - one이 트루이면 위에 리턴 rv[0]이 있으면 이미 중복됐다.(?) -다시 보면서 공부
            return "<script>alert('join fail');history.back(-1);</script>"  

        sql = "insert into user(id,password) values('%s', '%s')" % (id, pw)  ## id가 이미 데이터베이스에 없을 경우에는 값을 데이터베이스에 저장해줌.
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

    return render_template("join.html")                  ## /join으로 주소를 치고 들어왔을 때(GET방식), join으로 리턴

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

                  
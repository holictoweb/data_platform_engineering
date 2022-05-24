# flask 프로젝트 생성 

```py
app.py 생성

python app.py
```


# flask 설치 

```bash
pip instal flask

```


# basic flask
- app.py 생성
  
```python
# Flask import
from flask import Flask
# app 객체 생성
app = Flask(__name__)
# 라우터 설정
@app.route("/hello")  
def hello():
    return  "<h1>Hello Flask!</h1>"
# 웹 서버 구동
if __name__ == '__main__': # 모듈이 아니라면, 웹서버를 구동시켜라!
    app.run(host="0.0.0.0", port="8082")


- http://12.20.33.11/hello 호출 
```



# 구조 생성
## template 사용 

```py

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("zeppelin_dashboard.html")


@app.route('/crawling_history')
def crawling_history():
    return render_template("page_crawling_history.html")

@app.route('/synonyms')
def synonyms():
    return render_template("zeppelin_synonyms.html")

@app.route('/keywords')
def keywords():
    return render_template("zeppelin_keywords.html")


if __name__ == '__main__':
    host_addr = "0.0.0.0"
    port_num = '8082'
    app.run(host=host_addr, port=port_num)

```

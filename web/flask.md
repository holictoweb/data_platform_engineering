# flask 프로젝트 생성 

```py
app.py 생성

python app.py
```



# basic flask
- app.py
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
    app.run(host="127.0.0.1", port="8080")
```
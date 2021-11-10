# open api 



- 공공데이터 포탈

https://www.data.go.kr/index.do

- 인증키 

```
BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D
```



# DART 인증

5e99205e2b9885da9519dd55c253d9a7d70fbab3

```bash
# 코드 정보 조회
https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=5e99205e2b9885da9519dd55c253d9a7d70fbab3
```





# open api -> database

```python
# -*- conding:utf-8 -*-'
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import pymysql

startpg = 1
endpg = 1000
rows = []
key = '5e99205e2b9885da9519dd55c253d9a7d70fbab3'
for _ in range(12):
    url = f"http://openapi.seoul.go.kr:8088/[api key]/xml/busStopLocationXyInfo/{startpg}/{endpg}"

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    for i in soup.find_all('row'):
        rows.append({"stop_no": i.stop_no.string,
                     "stop_nm": i.stop_nm.string,
                     "xcode": i.xcode.string,
                     "ycode": i.ycode.string})
    startpg = endpg + 1
    endpg = endpg + 1000

columns = ["stop_no", "stop_nm", "xcode", "ycode"]
bus_stop_df = pd.DataFrame(rows, columns=columns)
# bus_stop_df
# bus_stop_df.to_csv("bus_stop.csv", mode='w', encoding='utf-8-sig', index=False)

engine = create_engine("mysql+mysqldb://<db id>:"+"<password>" +
                       "@<ip_address>/<db_name>?charset=utf8", encoding='utf8')
conn = engine.connect()

bus_stop_df.to_sql(name='<table_name>', con=engine,
                   if_exists='replace', index=False)
```





# api 사용방법





## 기업개황 API

https://opendart.fss.or.kr/api/company?crtfc_key=BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D

https://opendart.fss.or.kr/api/company.json?crtfc_key=BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D





https://opendart.fss.or.kr/api/corpCode.xml/BHI55TQtFP6CNuCQwbnJk0KO44OKicqy%2Ft0TTtjF6WvIEGS5OzxwItbF0STlJ%2B4v8G9egSBots4E6xF%2F4ATJig%3D%3D




# mysql + sqlalchemy connect 


## to_sql
```python
from sqlalchemy import create_engine
import pymysql
import pandas as pd
db_connection_str = 'mysql+pymysql://[db유저이름]:[db password]@[host address]/[db name]'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()


# 특정 테이블로 df 에서 저장

df.to_sql(name='db의 테이블이름', con=db_connection, if_exists='append',index=False)  


```




## read_sql 
```python
from sqlalchemy import create_engine
import pymysql
import pandas as pd
db_connection_str = 'mysql+pymysql://[db유저이름]:[db password]@[host address]/[db name]'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

df = pd.read_sql('SELECT * FROM api_storereview', con=conn) 
conn.close() # 커넥션 끊기


from sqlalchemy import create_engine
fngo_con_str = 'mysql+pymysql://fngo:2323@bigfinance-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/fngo'
fngo_engine = create_engine(fngo_con_str)
fngo_conn = fngo_engine.connect()
df = pd.read_sql('SELECT * FROM company', con=fngo_conn)

display(df)


# 읽어 오는 데이터에 대한 스키마 정의를 미리 할 수 있는지...


```




## delete data with alchemy
- to_sql  외에 쿼리 수행을 함께 진행 
```py
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

# save original records to 'records' table
df0.to_sql('records', con=engine)

# save updated records to 'records_updated' table
df.to_sql('records_updated', con=engine)

# delete updated records from 'records'
engine.execute("DELETE FROM records WHERE Id IN (SELECT Id FROM records_updated)")

# insert updated records from 'records_updated' to 'records'
engine.execute("INSERT INTO records SELECT * FROM records_updated")

# drop 'records table'
engine.execute("DROP TABLE records_updated")

# read from records
print(pd.read_sql('records', con=engine))

    Name Qualification
Id                    
1   Rick        Lawyer
2   John          Engg
5   mady        lawyer
3   Gini          Engg
4   Bist        Lawyer
```






# LOAD S3

```python



```


# multi column 
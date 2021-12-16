

# mysql + sqlalchemy connect 

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


```python
from sqlalchemy import create_engine
import pymysql
import pandas as pd
db_connection_str = 'mysql+pymysql://[db유저이름]:[db password]@[host address]/[db name]'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()
df = pd.read_sql('SELECT * FROM api_storereview', con=conn) # 여기서 sql문, 나는 api_storereview 테이블을 dataframe으로 전환
conn.close() # 커넥션 끊기
```


[install mysql](#install-mysql)



# Install MySQL

- 설치 
```bash
# 버젼 확인 
lsb_release -a


# mysql server 설치 - client도 함께 설치 
sudo apt-get install mysql-server

# 설치 후 path 에 대한 부분 확인 필요 

# 보안 관련 설정 ( root 비밀번호 설정 등 )
sudo mysql_secure_installation


```

- 실행 방법 
```bash
# mysql 실행 
sudo systemctl start mysql

# 
sudo /usr/bin/mysql -u root -p

```



# connection 

1. pymysql 연결
```python
import pymysql

#connect = pymysql.connect(host="", port=3306, user="", password="", db="")

connection = pymysql.connect(host='fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
                             user='mi_ro',
                             password='aicel2021!',
                             database='news',
                             cursorclass=pymysql.cursors.DictCursor)

# connect 에서 cursor 생성
cursors = connection.cursor()

# SQL문 실행
sql = "select * from news.gn_news_nlp_job where flag='0'"
cursors.execute(sql)

# data fetch
data = cursors.fetchall()
print(data)
# connection 닫기
connection.close()

```

2. sqlalchemy 연결
```py

fngo_con_str = 'mysql+pymysql://fngo:fngofinance@bigfinance-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/fngo'
fngo_engine = create_engine(fngo_con_str)
fngo_con = fngo_engine.connect()
# read
df_gn_company = pd.read_sql('select * from gn_company', con=news_con )
# write
df_sync.to_sql(name='gn_{}'.format(table), con=news_con, if_exists='append', index=False)
```   


# 테이블 별 사이즈 확인 
```sql
 SELECT table_name AS 'TableName',
                 ROUND(SUM(data_length+index_length)/(1024*1024), 2) AS 'All(MB)',
                 ROUND(data_length/(1024*1024), 2) AS 'Data(MB)',
                 ROUND(index_length/(1024*1024), 2) AS 'Index(MB)'
FROM information_schema.tables
where  TABLE_SCHEMA = 'news'
GROUP BY table_name
ORDER BY data_length DESC; 
```
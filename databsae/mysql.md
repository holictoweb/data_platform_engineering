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



# USER

```sql

CREATE USER 'aicel'@'%' identified by 'Aicel2021!';


GRANT ALL PRIVILEGES ON *.* TO 'aicel'@'%'

```

- 비밀번호 변경
```sql
-- MySQL 5.7 이상
UPDATE mysql.user SET authentication_string=PASSWORD('Aicel2021!') WHERE User='root' AND Host='localhost';
FLUSH PRIVILEGES;


-- mysql 8.0
alter user 'root'@'lacalhost' identified with mysql_native_password by 'Aicel';

```




# MySQL Management 


```sql
-- 세션 상태 확인 
select count(*) from information_schema.processlist where command='Sleep';



```
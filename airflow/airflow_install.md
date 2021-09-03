# airflow 설치 

```bash
sudo apt update
sudo apt upgrade

# pip 설치 필요시 
sudo apt-get install python3-pip

pip3 install --upgrade pip==20.2.4

# 환경변수 등록
export AIRFLOW_HOME=~/airflow

# 위에 방식으로 정상적으로 되지 않을 경우 
.bashrc 파일에  export AIRFLOW_HOME=~/airflow 추가 

source .bashrc


# 설치 후 path 지정 
PATH=$PATH:/home/ubuntu/.local/bin


# 문제 발생
#pip3 install apache-airflow
pip install apache-airflow==2.1.3 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.3/constraints-3.7.txt"



# airflow.cfg 내용을 수정하지 않으면 sqlite 로 설치 
# 다른 rdb로 변경 하더라도 일단 최초는 sqlite로 실행 후 기본적인 셋팅이 되어야 airflow.cfg 수정이 가능 
airflow db init


```



- mysql 설정 

```bash
# mysql 사용을 위해서 pymysql 설치 필요 
# sqlalchemy가 기본 연결 설정임
pip install pymysql
```
```sql
# 계정 생성
create user 'airflow'@'localhost' identified by 'aicel2021!';

# DB 권한 부여
grant all privileges on *.* to 'airflow'@'localhost';
grant all privileges on airflow.* to 'airflow'@'localhost';

# Database 생성
create database airflow;

flush privileges;
```

- 오류 발생 확인 
```bash 
pymysql.err.OperationalError: (1071, 'Specified key was too long; max key length is 3072 bytes')

#airflow db init 중 위와 같이 오류가 발생 할경우 charset 에 대한 확인 필요 
ALTER DATABASE `databasename` CHARACTER SET utf8; 

```



- config 변경

```python
# timezone 설정
# default_timezone = utc
default_timezone = Asia/Seoul

# executor = SequentialExecutor
executor = LocalExecutor

# MySQL Connection 설정
# sql_alchemy_conn = sqlite:////home/airflow/airflow/airflow.db
sql_alchemy_conn =  mysql+pymysql://airflow:Bespin12!@127.0.0.1:3306/airflow

# 비밀번호 사용
# auth_backend = airflow.api.auth.backend.deny_all
auth_backend = airflow.api.auth.backend.basic_auth

# catchup_by_default = True
catchup_by_default = False

```

- 작업이 모두 종료 된 후 사용자 생성 
```bash
# user 생성
airflow users create \
    --username aicel \
    --firstname lee \
    --lastname joonik \
    --role Admin \
    --email joonik.lee@aiceltech.com
```



# timezone
```
# timezone 에 대한 설정 확인 필요 


```



dag refresh



```bash
python3 -c "from airflow.models import DagBag; d = DagBag();"
```


<img src="https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2019/04/17/sagemaker-airflow-2.gif" alt="airflow archi" style="zoom: 150%;" />

# airflow 설치 


## 1. airflow 설치 
```bash
sudo apt update
sudo apt upgrade

# pip 설치 필요시 
sudo apt-get install python3-pip

pip3 install --upgrade pip==20.2.4
/usr/bin/python3 -m pip install --upgrade pip

# 환경 변수 적용 
# 설치 후 path 지정 - conda 환경일 경우 별도 conda env의 bin을 등록 

vi .bashrc

export AIRFLOW_HOME=~/airflow
PATH=$PATH:/home/ubuntu/.local/bin
export PATH=$PATH:~/.local/bin
export PATH=$PATH:/home/ubuntu/.local/bin

source .bashrc


# 문제 발생
#pip3 install apache-airflow

# 실제 적용 https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html
pip install apache-airflow==2.1.3 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.3/constraints-3.7.txt"

# constraint 파일의 버젼을 사용중인 python 버젼으로 지정 
pip install "apache-airflow[celery]==2.2.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.2/constraints-3.8.txt"

pip install "apache-airflow[celery]==2.2.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-3.8.txt"

# 일단 생성 후 아래 명령을 실행 해야 cfg 등 위에 설정한 airflow home이 적용되어
# 관련 설정이 생성됨. 
airflow db init 

# db 연결 후 airflow db 생성 
sudo apt install mysql-client-core-8.0
sudo apt install mysql-client-core-5.6


# 필요 라이브러리 설치
pip install pymysql
pip install SQLAlchemy
# celery backend_result 사용을 위해 db+mysql:
sudo apt-get install -y python3-mysqldb

# redis 사용을 위해 
pip install redis


# dag 용 라이브러리 설치 
pip install IPython
pip install bs4
pip install opensearch-py
pip install s3fs
pip install pymongo
pip install pandas
pip install boto3
pip install apache-airflow-providers-amazon


# airflow.cfg db 설정 확인
sql_alchemy_conn =  mysql+pymysql://admin:Aicel2022!@airflow-db-prod.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com:3306/airflow_db

# airflow.cfg 내용을 수정하지 않으면 sqlite 로 설치 
# 다른 rdb로 변경 하더라도 일단 최초는 sqlite로 실행 후 기본적인 셋팅이 되어야 airflow.cfg 수정이 가능 
airflow db init

# airflow user 생성 - db설정 까지 모두 끝난 후에 수행 
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
    
airflow users create \
    --username aicel \
    --firstname aicel \
    --lastname tech \
    --role Admin \
    --email joonik.lee@aiceltech.com
# 생성 
[2022-02-18 07:24:09,162] {manager.py:558} INFO - Added Permission menu access on Providers to role Admin
[2022-02-18 07:24:09,232] {manager.py:496} INFO - Created Permission View: can create on XComs
[2022-02-18 07:24:09,241] {manager.py:558} INFO - Added Permission can create on XComs to role Admin
Password:
Repeat for confirmation:
[2022-02-18 07:24:21,229] {manager.py:214} INFO - Added user aicel
User "aicel" created with role "Admin"


```

## 2. airflow service 등록 
```bash
# group  생성 
sudo groupadd airflow

# airflow 계정 생성 
sudo useradd -s /bin/bash airflow -g airflow -d /home/ubuntu/airflow -m

```
- env file 생성

```bash
vi /home/ubuntu/airflow/airflow.env

AIRFLOW_HOME=/home/ubuntu/airflow
PATH=/home/ubuntu/.local/bin
```

- service 등록


- airflow-webserver.service
```sh
[Unit]
Description=Airflow webserver
After=network.target

[Service]
Environment="PATH=/home/ubuntu/.local/bin:$PATH:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
EnvironmentFile=/home/ubuntu/airflow/airflow.env
User=ubuntu
Group=ubuntu
Type=simple
ExecStart=/home/ubuntu/.local/bin/airflow  webserver -p 8081
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target

```
- airflow-scheduler.service
```bash
[Unit]
Description=Airflow scheduler
After=network.target

[Service]
Environment="PATH=/home/ubuntu/.local/bin:$PATH:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
EnvironmentFile=/home/ubuntu/airflow/airflow.env
User=ubuntu
Group=ubuntu
Type=simple
ExecStart=/home/ubuntu/.local/bin/airflow scheduler
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target


```

- airflow-worker.service
```bash
[Unit]
Description=Airflow scheduler
After=network.target

[Service]
Environment="PATH=/home/ubuntu/.local/bin:$PATH:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
EnvironmentFile=/home/ubuntu/airflow/airflow.env
User=ubuntu
Group=ubuntu
Type=simple
ExecStart=/home/ubuntu/.local/bin/airflow celery worker
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target


```


- 위의 두개 파일을 사용하여 등록 
```bash
# service 등록 

sudo vi /etc/systemd/system/airflow-webserver.service
sudo vi /etc/systemd/system/airflow-scheduler.service

sudo vi /etc/systemd/system/airflow-worker.service

sudo chmod 755 airflow-webserver.service
sudo chmod 755 airflow-scheduler.service
sudo chmod 755 airflow-worker.service
sudo systemctl daemon-reload
sudo systemctl enable airflow-webserver.service
sudo systemctl enable airflow-scheduler.service
sudo systemctl enable airflow-worker.service

sudo systemctl start airflow-webserver.service
sudo systemctl start airflow-scheduler.service
sudo systemctl start airflow-worker.service

sudo systemctl stop airflow-webserver.service
sudo systemctl stop airflow-scheduler.service
sudo systemctl stop airflow-worker.service



sudo systemctl status airflow-webserver.service
sudo systemctl status airflow-scheduler.service
sudo systemctl status airflow-worker.service

# system log 확인 
sudo nano /var/log/syslog

# 실행 파일 airflow 에 대한 권한 변경 
chmod o+rx /home/ubuntu/.local/bin/airflow 


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


## 2. config 변경 (celery executor)

```python
[core]
# timezone 설정
# default_timezone = utc
default_timezone = Asia/Seoul

# executor = SequentialExecutor
executor = LocalExecutor

# MySQL Connection 설정
# sql_alchemy_conn = sqlite:////home/airflow/airflow/airflow.db
sql_alchemy_conn =  mysql+pymysql://airflow:Bespin12!@127.0.0.1:3306/airflow

broker_url = redis://aicel-airflow-redis-prod.vrin4n.0001.apn2.cache.amazonaws.com:6379/0

result_backend =  db+mysql://admin:Aicel2022!@airflow-db-prod.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com:3306/airflow_db

# 비밀번호 사용 # 설정 시 로그인을 위한 사용자 생성 필요 ( 추가 config 변경은 필요 없음 )
# auth_backend = airflow.api.auth.backend.deny_all
auth_backend = airflow.api.auth.backend.basic_auth

# catchup_by_default = True
catchup_by_default = False

load_examples = False

# dag 안의 동시 수행 task 갯수 지정 
dag_concurrency = 50
worker_concurrency = 50

# worker 와는 별도로 병렬 처리에 대한 처리는 parallelism
parallelism = 32

# How long before timing out a python file import
dagbag_import_timeout = 60.0

[werbserver]
default_ui_timezone = Asia/Seoul

# worker 와 webserver key가 동일해야 log 확인 가능 
secret_key = fH4i5JVisLhJHWy/o2UMsw==

```

### AWS 연결 
[airflow aws 연결](!https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)

- 일단 access key / secret key 베이스로 설정 
```yaml
# connection 설정 

```


- 작업이 모두 종료 된 후 사용자 생성 
```bash
# user 생성
airflow users create \
    --username aicel-airflow \
    --firstname lee \
    --lastname joonik \
    --role Admin \
    --email joonik.lee@aiceltech.com

# user 삭제
airflow users create \
    --username aicel-airflow \
    --firstname lee \
    --lastname joonik \
    --role Admin \
    --email joonik.lee@aiceltech.com
```





### dag refresh

```bash
python3 -c "from airflow.models import DagBag; d = DagBag();"
```
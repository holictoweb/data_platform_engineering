# airflow 설치 


## 1. airflow 설치 
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


# 설치 후 path 지정 - conda 환경일 경우 별도 conda env의 bin을 등록 
PATH=$PATH:/home/ubuntu/.local/bin
export PATH=$PATH:~/.local/bin
export PATH=$PATH:/home/ubuntu/.local/bin


# 문제 발생
#pip3 install apache-airflow
pip install apache-airflow==2.1.3 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.3/constraints-3.7.txt"



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
```

## 2. airflow service 등록 
```bash
# group  생성 
sudo groupadd airflow

# airflow 계정 생성 
sudo useradd -s /bin/bash airflow -g airflow -d /home/ubuntu/airflow -m

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

- 위의 두개 파일을 사용하여 등록 
```bash
# service 등록 

sudo vi /etc/systemd/system/airflow-webserver.service


sudo chmod 755 airflow-webserver.service
sudo chmod 755 airflow-scheduler.service
sudo systemctl daemon-reload
sudo systemctl enable airflow-webserver.service
sudo systemctl enable airflow-scheduler.service

sudo systemctl start airflow-webserver.service
sudo systemctl start airflow-scheduler.service

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


## 2. config 변경

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

# 비밀번호 사용 # 설정 시 로그인을 위한 사용자 생성 필요 ( 추가 config 변경은 필요 없음 )
# auth_backend = airflow.api.auth.backend.deny_all
auth_backend = airflow.api.auth.backend.basic_auth

# catchup_by_default = True
catchup_by_default = False



# dag 안의 동시 수행 task 갯수 지정 
dag_concurrency = 50
worker_concurrency = 50

# worker 와는 별도로 병렬 처리에 대한 처리는 parallelism
parallelism = 32

# How long before timing out a python file import
dagbag_import_timeout = 60.0

[werbserver]
default_ui_timezone = Asia/Seoul

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
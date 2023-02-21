# Airflow Setting Guide

Airflow 구축 전에 반드시 해야할 것 중에 하나는 Airflow Home 경로를 설정하는 것입니다. 

저의 경우에 는 항상 경로 세팅을 나중에 하다가 잊어버려서 에러가 나는 경우가 많아서 꼭 먼저 설정해두곤 합니다. 

![airflow quick](airflow quick.png)

Airflow 공식 문서에 따르면 기본 경로는 위 사진에 나와있는 것과 같습니다. 그냥 놔둬도 되지만 나중에 경로를 옮길 때를 대비해서 한번 세팅해봅시다. 

```sh
# EC2
export AIRFLOW_HOME=/home/ec2-user/airflow
```

## 1. Redis 세팅 

이제 브로커로 사용할 Redis를 설치해 줍시다. 

```sh
sudo amazon-linux-extras install epel -y
# 위의 명령어 수행시 repo 충돌로 인하여 yum 실행이 불가합니다.
# yum 미 수행 이유는 aws 이외의 repo가 존제 하기 떄문입니다.
# amzn2-extras.repo & amzn2-core.repo 를 제외한 file을 다른 경로로 이동 해주세요.

sudo su
cd /etc/yum.repos.d
ls -alth
# amzn2-extras.repo
# amzn2-core.repo
# epel-testing.repo  
# epel.repo

# epel.repo 경로 이동
mkdir bk-epel-repo
mv epel* bk-epel-repo/
mv bk-epel-repo ../

# epel repo 이동 완료 후 yum 작동 확인
yum list

# redis 설치 
sudo amazon-linux-extras install redis4.0 -y
```

Redis의 configure 파일을 수정합니다. 

```sh
sudo vim /etc/redis.conf
#/etc/redis.conf 
[..] 
daemonize yes 
[..] 

[..] 
bind 0.0.0.0 
[..] 
```

airflow 부팅시 자동실행하기 추가 

```sh
# 자동 실행 추가
sudo chkconfig redis on 
sudo chkconfig redis-sentinel on
# 자동 실행 list 확인
systemctl list-unit-files | grep redis
```

서버 실행!

```sh
sudo service redis start 
# 강제 종료시 
sudo service redis stop 
```

실제로 돌아가는 프 로세스가 있는지 확인합니다. `ps -ef | grep redis` 제대로 세팅이 되었다면 
다음과 같이 나올 것입니다. 

![redis_on](redis_on.png)

Redis가 돌아가고 있다 브로커는 구축이 되었습니다. 

## 2. MySQL 세팅 

Airflow 구축을 하면서 가장 삽질도 많이 하고 시간을 많이 낭비한 부분입니다. 
익숙하지 않아서인지 이 상하게 MySQL을 다룰 때마다 에러 핸들링을 오래 하게 되는 것 같습니다. 
MySQL 설치

```sh
sudo yum install mysql -y
# 폐쇄망일 경우 수동 설치 필요 (https://dev.mysql.com/downloads/mysql/5.7.html)
# 직접 다운 받은 tar 압축해제
tar -xvf mysql-5.7.34-el7-x86_64.tar
ls -alth
# -rw-r--r-- 1 ec2-user ec2-user 697M Mar 26 07:27 mysql-5.7.34-el7-x86_64.tar.gz
# 다운로드 결과 다시 압축 해제
tar -xvzf mysql-5.7.34-el7-x86_64.tar.gz
# 결과물 경로 이동
mv mysql-5.7.34-el7-x86_64 /var/lib/
# 이름 변경
mv mysql-5.7.34-el7-x86_64 mysql

# MYSQL USER & GROUP 생성 
sudo su
groupadd mysql
useradd -g mysql mysql

# mysql 폴더 생성 및 권한 변경 
cd /var/lib/mysql
mkdir data logs
chown -R mysql:mysql data 
chown -R mysql:mysql logs
chomod 775 data logs

# /etc/my.cnf 생성 
vi /etc/my.cnf
=====================================
[client]
default-character-set=utf8
port=3306
socket=/var/lib/mysql/mysql.sock
default-character-set=utf8


[mysqld]
socket=/var/lib/mysql/mysql.sock
basedir=/var/lib/mysql
datadir=/var/lib/mysql/data
user=mysql
key_buffer_size=64M
max_allowed_packet=32M
query_cache_size=32M
max_connections=2625
max_connect_errors=2000000
wait_timeout=60

explicit_defaults_for_timestamp = 1
pid-file=/var/lib/mysql/mysqld.pid
log-error=/var/lib/mysql/logs/mysqld.log
character-set-server=utf8
collation-server=utf8_general_ci

bulk_insert_buffer_size=0
=====================================

chown mysql:mysql /etc/my.cnf

# my.cnf 초기화 / Mysql 실행
cd /var/lib/mysql/bin
./mysqld --defaults-file=/etc/my.cnf --initialize
./mysqld --defaults-file=/etc/my.cnf &

# mysql 최초 접속 password 확인
cat /var/lib/mysql/logs/mysqld.log | grep password
# 2021-05-14T04:19:07.295807Z 1 [Note] A temporary password is generated for root@localhost: #t%=3oAu0uN&

# MySQL 접속
# 사용자 변경
yum install -y ncurses*
su mysql
cd /var/lib/mysql/bin
./mysql -u root -p
# Password : 3oAu0uN&
```

```sql
-- Mysql QUERY
SET PASSWORD = PASSWORD('Bespin12!');
use mysql;

SET GLOBAL explicit_defaults_for_timestamp = 1;

flush privileges;

-- 사용자 생성
create user 'airflow'@'localhost' identified by 'Bespin12!';


-- DB 권한 부여
grant all privileges on *.* to 'airflow'@'localhost';
grant all privileges on airflow.* to 'airflow'@'localhost';


-- database 생성
create database airflow;
flush privileges;


-- database 확인 
show databases;
```

```sh
# mysql.server 등록
sudo su
cd /var/lib/mysql/support-files
cp /var/lib/mysql/support-files/mysql.server /etc/init.d/mysql.server
chkconfig --add mysql.server
chmod +x /etc/init.d/mysql.server
chkconfig --list
chkconfig mysql.server on

# 프로세스 확인 
ps -ef | grep mysqld
```

```sh
# mysql /etc/profile 등록  

##############################################################################################################
# mysql 수동 설치 이므로 mysql bin 경로 이외의 경로에서 mysql 수행시 아래의 결과 출력 
##############################################################################################################
[root@ init.d]# mysql -uroot -pBespin12!
bash: mysql: command not found
##############################################################################################################

sudo su
vi /etc/profile

# 제일 하단에 추가
export MYSQL_HOME=/=/usr/local/mysql
export PATH="$PATH:/var/lib/mysql/bin"

source /etc/profile
```

설치가 완료되면 mysql 데몬을 실행합니다. 

```sh
sudo service mysqld start mysqld
```

험난 했던 MySQL 세팅은 완료되었습니다. 

## 3. Airflow 설치 및 세팅

이제 Airflow를 설치해봅시다. 

```sh
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel
python3-devel.x86_64 cyrus-sasl-devel.x86_64 -y
sudo yum install gcc -y
sudo yum install libevent-devel -y
sudo python3 -m pip install --upgrade pip
pip3 install wheel
pip3 install boto3 PyMySQL celery flask-bcrypt
pip3 install "SQLAlchemy==1.3.15"
pip3 install apache-airflow==1.10.14
pip3 install 'apache-airflow[mysql]==1.10.14'
pip3 install 'apache-airflow[aws]==1.10.14'
pip3 install 'apache-airflow[celery]==1.10.14'
pip3 install 'apache-airflow[redis]==1.10.14'
# Optional
sudo python3 -m pip install 'apache-airflow-backport-providers-google[amazon]'
```

설치가 완료되었다면 airflow 폴더애 있는 airflow.cfg를 수정해서 앞서 설치한 redis와 mysql을 airflow 와 이어줘야 합니다.
 **하지만 아무리 찾아봐도** **airflow** **폴터가 보이지 않습니다. 분명히 설치를 했는데!** 
airflow를 입력해서 airflow 명령어가 동작하는지 먼저 확인합니다.  `airflow db init`
만약 명령어가 작동한다면 아까 설정 해둔 AIRFLOW_HOME 경로에 airflow 폴더가 생성될 것입니다. 
그 안에 configuration 파일이 있습니다. 
**airflow.cfg 설정** 

```sh
cd airflow
vim airflow.cfg
```

```sh
# 사용할 dag 폴더 지정
# subfolder in a code repository. This path must be absolute. 꼭 절대경로!
dags_folder = /home/ec2-user/airflow/dags
# executor = SequentialExecutor
executor = LocalExecutor
# sql_alchemy_conn = sqlite:////home/airflow/airflow/airflow.db
sql_alchemy_conn = mysql+pymysql://airflow:Bespin12!@127.0.0.1:3306/airflow
# catchup_by_default = True
catchup_by_default = False
# broker_url = sqla+mysql://airflow:airflow@127.0.0.1:3306/airflow
broker_url = redis://localhost:6379/0
# result_backend = db+mysql://airflow:airflow@localhost:3306/airflow
result_backend = db+mysql://airflow:Bespin12!@127.0.0.1:3306/airflow
# auth_backend = airflow.api.auth.backend.deny_all
auth_backend = airflow.contrib.auth.backends.password_auth
# load_examples = True
load_examples = False
rbac = True
```

이 정도만 세팅 해줍니다. 

실행에 필요한 라이브러를 설치해주고 

airflow db를 초기화 해봅시다. 

```sh
airflow db init
```

Done!이 나왔다면 성공입니다. 

```sh
# db initialize
airflow initdb
# user 생성
airflow users create -r Admin -u jungmin -p Bespin12! -e jungmin.choi@bespinglobal.com -f jungmin -l choi
# dag 목록 조회
airflow list_dags
```

Setting 끝!!!! 

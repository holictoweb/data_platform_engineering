#  zeppelin install

##  jdk 설치 

```bash
# JDK 설치 
sudo apt install openjdk-8-jre-headless

# JAVA_HOME 위치 확인
which java 
> /usr/bin/java
readlink -f /usr/bin/java
> /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

# JAVA_HOME 추가 - 안됨.. 걍 export 함
vi /etc/profile

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```



```bash
# zepplein 설치
wget https://dlcdn.apache.org/zeppelin/zeppelin-0.10.0/zeppelin-0.10.0-bin-all.tgz

# 압축해제
tar -xzvf zeppelin-0.10.0-bin-all.tgz 

# zepplein 실행



```

## 환경 설정

- zeppelin-site.xml 
- 실행 후 접근 시 wsl 은 localhost:8888

```xml
<property>
  <name>zeppelin.server.addr</name>
  <value>0.0.0.0</value>
  <description>Server binding address</description>
</property>

<property>
  <name>zeppelin.server.port</name>
  <value>8888</value>
  <description>Server port.</description>
</property>
```



```bash

# 필요한 부분 설정 필요 

export JAVA_HOME=C:\Program Files\Java\jdk1.8.0_201
export SPARK_HOME=C:\HadoopEco\spark-2.4.7-bin-hadoop2.7
export PYSPARK_PYTHON=C:\HadoopEco\spark-2.4.7-bin-hadoop2.7\python

# 실제 spark을 사용하지 않기에 아래 내용으로 설정 
export PYTHONPATH=C:\HadoopEco\spark-2.4.7-bin-hadoop2.7\python
```



_ _ _

# 실행 

```bash
bin/zeppelin-daemon.sh stop
bin/zeppelin-daemon.sh start
bin/zeppelin-daemon.sh status
```



- python 기반으로 실행 하기 위해 아래 install 

```bash
pip install jupyter
pip install grpcio
pip install protobuf
```

- python 사용을 위해 우측 상단 프로필을 클릭 후 interperter 에서 python 을 찾은 후 zeppelin.python 의 실행 위치를 conda 환경으로 변경



mongo --host tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017 --username root --password "01234567890"

# cron 사용

- cron 사용을 위해 활성화 및 특정 폴더에 있는 노트북만 사용 하도록 폴더 설정 가능 

```xml
<property>
  <name>zeppelin.notebook.cron.enable</name>
  <value>true</value>
  <description>Notebook enable cron scheduler feature</description>
</property>
<property>
  <name>zeppelin.notebook.cron.folders</name>
  <value></value>
  <description>Notebook cron folders</description>
</property>
```



# shiro login

- id / pw 생성

```python
# zeppelin/conf/shiro.ini
shiro.ini.template 를 복사 하여 생성

[users]
# List of users with their password allowed to access Zeppelin.
# To use a different strategy (LDAP / Database / ...) check the shiro doc at http://shiro.apache.org/configuration.html#Configuration-INISections
# To enable admin user, uncomment the following line and set an appropriate password.
#admin = password1, admin
user1 = password2, role1, role2
user2 = password3, role3
user3 = password4, role2

```

- role 생성 



# mysql interpreter 연결

- jdbc 커넥터 라이브러리 필요 

```bash
# default lib
ubuntu@62:~/zeppelin/interpreter/jdbc$ ls
META-INF  ansi.sql.keywords  interpreter-setting.json  postgresql-native-driver-sql.keywords  zeppelin-jdbc-0.10.0.jar
```

- mysql connector 설치

```bash
# mysql 버젼 확인 후 동일 버젼 사용 
wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.11.tar.gz
```

[mysql document](https://zeppelin.apache.org/docs/latest/interpreter/jdbc.html#mysql)

- create interpreter
- zepplin 이 세션을 잡은 이후 8시간 ( mysql timeout 설정 ) 이후 connection 이 끊기는 현상으로 연결 마다 신규 생성 하는 형태로 추가 필요 

#####  Properties

|       Name       |                        Value                        |
| :--------------: | :-------------------------------------------------: |
|  default.driver  |                com.mysql.jdbc.Driver                |
|   default.url    | jdbc:mysql://localhost:3306?**autoReconnect**=true/ |
|   default.user   |                     mysql_user                      |
| default.password |                   mysql_password                    |

##### Dependencies

|             Artifact              | Excludes |
| :-------------------------------: | :------: |
| mysql:mysql-connector-java:8.0.11 |          |



# documentdb interpretor 연결

- jdbc 커넥터 설정

```
	
```

- documentdb jdbc driver download

- https://github.com/aws/amazon-documentdb-jdbc-driver/releases

```python
mongodb://root:<insertYourPassword>@tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false


mongodb://root:<insertYourPassword>@tf-dev-docdb-cluster-vst-0.c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017/?retryWrites=false
```



```

```

# zeppelin output

## output limit (X)

```
zeppelin.interpreter.output.limit = 102400000
zeppelin.websocket.max.text.message.size = 102400000
```



_ _ _



# zeppelin notebook api 

https://zeppelin.apache.org/docs/0.10.0/usage/rest_api/notebook.html




# kafak connector 설치 
- 내용 추후 확인 필요 https://mongsil-jeong.tistory.com/35

- https://packages.confluent.io/archieve/6.1/ 
```bash


```




# custom connect plugin 등록
1. mysql connect download 
    - [실제 다운로드](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc?_ga=2.192985453.1155617456.1665478996-1952939441.1665478996&_gac=1.116139764.1665479176.CjwKCAjwqJSaBhBUEiwAg5W9p9igaKaW9KjosN05V7907wBqvgP-7D1rsk7wjecfkvZSLFNTYYr2XxoC-MMQAvD_BwE) 
    - (base) ubuntu@ip-10-0-2-115:~/download/confluentinc-kafka-connect-jdbc-10.6.0/lib$ pwd
/home/ubuntu/download/confluentinc-kafka-connect-jdbc-10.6.0/lib 아래와 같은 jar 파일 목록 확인
    - 
```bash 
checker-qual-3.5.0.jar          ons-19.7.0.0.jar        slf4j-api-1.7.36.jar
common-utils-6.0.0.jar          oraclepki-19.7.0.0.jar  sqlite-jdbc-3.25.2.jar
jtds-1.3.1.jar                  orai18n-19.7.0.0.jar    ucp-19.7.0.0.jar
kafka-connect-jdbc-10.6.0.jar   osdt_cert-19.7.0.0.jar  xdb-19.7.0.0.jar
mssql-jdbc-8.4.1.jre8.jar       osdt_core-19.7.0.0.jar  xmlparserv2-19.7.0.0.jar
ojdbc8-19.7.0.0.jar             postgresql-42.3.3.jar
ojdbc8-production-19.7.0.0.pom  simplefan-19.7.0.0.jar 
```
    - (스키마레지스트리추가) 다운받아서 linux 상에서 schema-registry jar을 추가 하여 재 압축 필요 ( 전체 폴더 압축 )
2. aws-schema-registry / mysql-connector 두개에서 필요 jar 다운로드 
    - aws s3 cp s3://aicel-workflow/prod/kafka/confluentinc-kafka-connect-jdbc-10.6.0.zip .
3. aws-schema-registry / mysql-connector-java-8.0.11 / avro-kafkaconnect-converter ( maven project 중 확인 ) - 해당 jar 파일을 모아서 압축 
4. upload s3 
   - 압축된 zip 파일을 s3 업로드 
5. create msk custom plugin 
   - plugin 생성 

# source connector 생성

```conf 
tasks.max=1
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
connection.url=jdbc:mysql://fngo-ml-rds-cluster-8-cluster.cluster-c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com:3306/news?verifyServerCertificate=false&useSSL=false
connection.user=fngoMLAdmin
connection.password=fngo_2020-for!Knowledge
topic.prefix=news.naver.
poll.interval.ms=10000
table.whitelist=gn_news_company_table
mode=timestamp
timestamp.column.name=published_at
timestamp.initial=-1
time.precision.mode=connect


# prefix를 지정하고 table 명이 뒤에 붙는 방식이지만 실제 topic 자체는 자동 생성은 하지 않음. 
# timestamp.initial -1 현재 시점 부터 


# topic 설정시 추가 참고 
topic.regex=news.naver* 
topic.prefix=news.naver.gn_news_company_table
```


#  TEMP
- https://cjw-awdsd.tistory.com/53
```json 
{
    "name": "my-source-connect",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "connection.url": "jdbc:mysql://localhost:3306/test",
        "connection.user":"root",
        "connection.password":"비밀번호",
        "mode":"incrementing",
        "incrementing.column.name" : "id",
        "table.whitelist" : "users",
        "topic.prefix" : "example_topic_",
        "tasks.max" : "1",
    }
}
cUrl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"

```


- name : source connector 이름(JdbcSourceConnector를 사용)
- config.connector.class : 커넥터 종류(JdbcSourceConnector 사용)
- config.connection.url : jdbc이므로 DB의 정보 입력
- config.connection.user : DB 유저 정보
- config.connection.password : DB 패스워드
- config.mode : "테이블에 데이터가 추가됐을 때 데이터를 polling 하는 방식"(bulk, incrementing, - timestamp, timestamp+incrementing)
- config.incrementing.column.name : incrementing mode일 때 자동 증가 column 이름
- config.table.whitelist : 데이터를 변경을 감지할 table 이름
- config.topic.prefix : kafka 토픽에 저장될 이름 형식 지정 위 같은경우 whitelist를 뒤에 붙여 example_topic_users에 데이터가 들어감
- tasks.max : 커넥터에 대한 작업자 수(본문 인용.. 자세한 설명을 찾지 못함)
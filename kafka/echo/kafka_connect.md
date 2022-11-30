# kafak connector 설치 
- 내용 추후 확인 필요 https://mongsil-jeong.tistory.com/35
- 
- https://packages.confluent.io/archieve/6.1/ 
```bash
# 현재 사용 가능한 connector plugin 조회
curl http://localhost:8083/connector-plugins | python -m json.tool

# mysql connector JDBC 설치
wget kafka-connect-jdbc:10.5.0

```




# aws msk connect 문서
- https://aws.amazon.com/ko/blogs/korea/introducing-amazon-msk-connect-stream-data-to-and-from-your-apache-kafka-clusters-using-managed-connectors/


이러한 설정 중 일부는 일반적인 설정으로서, 모든 커넥터에 대해 지정해야 합니다. 예를 들면 다음과 같습니다.

connector.class는 커넥터의 Java 클래스입니다.
tasks.max는 이 커넥터에 대해 생성되어야 할 태스크의 최대 수입니다.
다른 설정은 Debezium MySQL 커넥터에만 해당됩니다.

database.hostname은 Aurora 데이터베이스의 작성자 인스턴스 엔드포인트를 포함합니다.
database.server.name은 데이터베이스 서비의 논리적 이름입니다. 이 설정은 이름은 Debezium에서 생성한 Kafka 주제의 이름에 사용됩니다.
database.include.list는 지정한 서버에서 호스팅하는 데이터베이스의 목록을 포함합니다.
database.history.kafka.topic은 데이터베이스 스키마 변경을 추적하기 위해 Debezium에서 내부적으로 사용하는 Kafka 주제입니다.
database.history.kafka.bootstrap.servers는 MSK 클러스터의 부트스트랩 서버를 포함합니다.
마지막의 8개 줄(database.history.consumer.* 및 database.history.producer.*)은 데이터베이스 기록 주제를 액세스하기 위한 IAM 인증을 활성화합니다.





# debizium 파라미터 설명
- https://docs.confluent.io/debezium-connect-mysql-source/current/mysql_source_connector_config.html

- database.include.list 
  - An optional comma-separated list of regular expressions that match database names to be monitored.
- table.include.list 
  - Each identifier is of the form schemaName.tableName

## sample 
```conf 
connector.class=io.debezium.connector.mysql.MySqlConnector
database.user=fngoMLAdmin
database.server.id=123456
tasks.max=1
database.history.kafka.topic=news.naver.gn_news_company.history
database.history.kafka.bootstrap.servers=b-2.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092
database.server.name=news
database.port=3306
include.schema.changes=true
database.hostname=fngo-ml-rds-cluster-8-cluster.cluster-c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com
database.password=fngo_2020-for!Knowledge
table.include.list=news.gn_news_company
database.include.list=news
```



# jdbc connect
- source connector confluent doc
  - 설정 옵션들
  - https://docs.confluent.io/kafka-connect-jdbc/current/source-connector/source_config_options.html

## mysql connector 설치
wget kafka-connect-jdbc:10.5.0

- https://docs.confluent.io/kafka-connect-jdbc/current/index.html
- 실제 적용을 위해서 각 db별 connector 설치가 필수로 필요함. 확인 필요 
- mysql 연결 ( https://docs.confluent.io/kafka-connect-jdbc/current/index.html#mysql-server  )

## jdbc deep dive confluent doc
- https://www.confluent.io/blog/kafka-connect-deep-dive-jdbc-source-connector/


## option




```python

# 아래와 같이 컨버터 설정 하는 방법도 있지만 설정으로 처리 
"transforms.TimestampConverter.format": "yyyy-MM-dd HH:mm:ss.SSSSSS",
"transforms.TimestampConverter.target.type": "Timestamp",
"transforms.TimestampConverter.field ": "date3",


time.precision.mode=connect
``` 

## sample 
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

## sampel default 
- https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect-connectors.html 

```conf
connector.class=io.confluent.connect.s3.S3SinkConnector
tasks.max=2
topics=my-example-topic
s3.region=us-east-1
s3.bucket.name=my-destination-bucket
flush.size=1
storage.class=io.confluent.connect.s3.storage.S3Storage
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
key.converter=org.apache.kafka.connect.storage.StringConverter
value.converter=org.apache.kafka.connect.storage.StringConverter
schema.compatibility=NONE
```


- - - 

# WORKER  Configuration
##  with Schema Registry

```conf
key.converter.region=ap-northeat-2
key.converter.schemaAutoRegistrationEnabled=true
key.converter.avroRecordType=GENERIC_RECORD

value.converter.region=ap-northeat-2
value.converter.schemaAutoRegistrationEnabled=true
value.converter.avroRecordType=GENERIC_RECORD

value.converter.schema.registry.url=http://someIP:8081
value.converter.registry.name=Glue-Schema-Registry
value.converter.schemaName=my-topic-schema
value.converter=io.confluent.connect.avro.AvroConverter

value.converter.enhanced.avro.schema.support=true
<>

// schema.compatibility=BACKWARD

```

# Connect integration with glue schema registry 
- https://github.com/awslabs/aws-glue-schema-registry

```conf
key.converter=org.apache.kafka.connect.storage.StringConverter
key.converter.schemas.enable=False
value.converter=com.amazonaws.services.schemaregistry.kafkaconnect.AWSKafkaAvroConverter
value.converter.region=ap-northeast-2
value.converter.schemaAutoRegistrationenabled=true
value.converter.avrorecordtype=GENERIC_RECORD
value.converter.schemaname=gn_news_company_table
value.converter.registry.name=news.naver

# value.converter.enhanced.avro.schema.support=true
# schema.compatibility=BACKWARD

```


## Apache kafka connect
- https://docs.aws.amazon.com/glue/latest/dg/schema-registry-integrations.html#schema-registry-integrations-apache-kafka-connect


- 가장 유사한 내용이 많아 보이는 샘플
- https://stackoverflow.com/questions/69941470/how-to-fix-msk-connector-glue-registry-timeout-error
```conf
connector.class=io.confluent.connect.s3.S3SinkConnector
s3.region=eu-west-1
flush.size=1
schema.compatibility=FULL
tasks.max=2
topics=awsuseravro1
format.class=io.confluent.connect.s3.format.avro.AvroFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
storage.class=io.confluent.connect.s3.storage.S3Storage
s3.bucket.name=hfs3testing

topics.dir=avrotopics1

value.converter=com.amazonaws.services.schemaregistry.kafkaconnect.AWSKafkaAvroConverter
value.converter.region=ap-northeast-2
value.converter.schemaAutoRegistrationEnabled=true
value.converter.avroRecordType=GENERIC_RECORD
value.converter.schemaName=gn_news_company_table
value.converter.registry.name=news.naver

```


- 기본 설정 내용 
```conf
key.converter.region=aws-region
value.converter.region=aws-region
key.converter.schemaAutoRegistrationEnabled=true
value.converter.schemaAutoRegistrationEnabled=true
key.converter.avroRecordType=GENERIC_RECORD
value.converter.avroRecordType=GENERIC_RECORD
```

# 자동 설정 형태 인것으로 보임 
```conf 
key.converter=org.apache.kafka.connect.storage.StringConverter
key.converter.schemas.enable=False
value.converter.region=ap-northeast-2
value.converter.schemaAutoRegistrationEnabled=true
value.converter.avroRecordType=GENERIC_RECORD
```


## default 
```json
key.converter=org.apache.kafka.connect.storage.StringConverter
key.converter.schemas.enable=False
value.converter=org.apache.kafka.connect.json.JsonConverter
value.converter.schemas.enable=True

```

# producer glu schema registry
- https://github.com/awslabs/aws-glue-schema-registry#using-the-aws-glue-schema-registry-library-serializer--deserializer
```java

        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, GlueSchemaRegistryKafkaSerializer.class.getName());
        properties.put(AWSSchemaRegistryConstants.DATA_FORMAT, DataFormat.AVRO.name());
        properties.put(AWSSchemaRegistryConstants.AWS_REGION, "us-east-1");
        properties.put(AWSSchemaRegistryConstants.REGISTRY_NAME, "my-registry");
        properties.put(AWSSchemaRegistryConstants.SCHEMA_NAME, "my-schema");

```


## confluent jdbc source connector document
- https://docs.confluent.io/kafka-connect-jdbc/current/source-connector/index.html

"connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
"connection.url": "jdbc:mysql://mysql:3306/test",
"connection.user": "connect_user",
"connection.password": "connect_password",
"topic.prefix": "mysql-01-",
"poll.interval.ms" : 3600000,
"table.whitelist" : "test.accounts",
"mode":"bulk",

## mysql connect ERROR

```bash
2022-08-05T13:32:45.000+09:00	[Worker-04e41ddfde0db7b0e] [2022-08-05 04:32:45,083] INFO [aicel-news-jdbc-source-connector-prod|task-0] Using JDBC dialect MySql (io.confluent.connect.jdbc.source.JdbcSourceTask:127)
2022-08-05T13:32:45.000+09:00	[Worker-04e41ddfde0db7b0e] [2022-08-05 04:32:45,084] INFO [aicel-news-jdbc-source-connector-prod|task-0] Attempting to open connection #1 to MySql (io.confluent.connect.jdbc.util.CachedConnectionProvider:79)
2022-08-05T13:32:45.000+09:00	[Worker-04e41ddfde0db7b0e] Fri Aug 05 04:32:45 UTC 2022 WARN: Establishing SSL connection without server's identity verification is not recommended. According to MySQL 5.5.45+, 5.6.26+ and 5.7.6+ requirements SSL connection must be established by default if explicit option isn't set. For compliance with existing applications not using SSL the verifyServerCertificate property is set to 'false'. You need either to explicitly disable SSL by setting useSSL=false, or set useSSL=true and provide truststore for server certificate verification.
2022-08-05T13:32:45.000+09:00	[Worker-04e41ddfde0db7b0e] Fri Aug 05 04:32:45 UTC 2022 WARN: Establishing SSL connection without server's identity verification is not recommended. According to MySQL 5.5.45+, 5.6.26+ and 5.7.6+ requirements SSL connection must be established by default if explicit option isn't set. For compliance with existing applications not using SSL the verifyServerCertificate property is set to 'false'. You need either to explicitly disable SSL by setting useSSL=false, or set useSSL=true and provide truststore for server certificate verification.
2022-08-05T13:32:45.000+09:00	[Worker-04e41ddfde0db7b0e] Fri Aug 05 04:32:45 UTC 2022 WARN: Caught while disconnecting...
2022-08-05T13:32:45.000+09:00	[Worker-04e41ddfde0db7b0e]


```






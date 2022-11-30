# kinesis Analytics 상에서 연결 생성

## aws supported connectors 
- flink-sql-connector-kinesis_2.12
- aws-msk-iam-auth
- flink-connector-kafka_2.12

### 추가 lib 설치 
- glue schema registry 
- avoro 사용 하기 위한 방법 확인 

## apache/flink github - avro-flue-schema-registry
- [github](https://github.com/apache/flink/tree/master/flink-formats)
- flink-formats/flink-avro-glue-schema-registry 프로젝트 빌드 후 라이브러리 등록 필요 
- flink-avro-glue-schema-registry_2.12-1.17-SNAPSHOT.jar (s3 업르도 후 추가 connector 로 등록 )
- 
### IAM 설정
- iam policy에 자동으로 생성되는 policy 확인 필요
  - kinesis-analytics-service-{생성한 stuido 이름}-ap-northeast-2
  

## 기본 api

![api 유형](https://velog.velcdn.com/images%2Fzxshinxz%2Fpost%2F56e78fb3-e18d-43b0-b2ee-e30d3b1f4b45%2F%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-08-15%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%2011.28.46.png)



<script src="https://gist.github.com/holictoweb/0aeddab0b566bcb2d1ae2eeec9b5269e.js"></script>
<script src="https://gist.github.com/holictoweb/94cd265defcead8d3e658db52568b71c.js"></script>
<script src="https://gist.github.com/holictoweb/94cd265defcead8d3e658db52568b71c.js"></script>\


## table 종류

- tamporary table / permanent table 

## SQL/Table API

- external table 생성의 형태로 topic 정보를 조회 

```python
%flink.ssql(type=update)
CREATE TABLE flink_avro_gn_news_company_table (
    news_url_md5 CHAR(32),
    company_code VARCHAR(7),
    ncc_flag VARCHAR(1),
    use_flag VARCHAR(1),
    published_at VARCHAR(30)
)
PARTITIONED BY (company_code)
WITH (
'connector'= 'kafka',
'topic' = 'news.gn_news_company_table',
'properties.bootstrap.servers' = 'b-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092, b-6.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092, b-5.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092',
'value.format' = 'avro',
'properties.group.id' = 'flink_consumer_group_news_prod_01'
-- 'scan.startup.mode'= 'earliest-offset'
);

```

- python
  
```py
%flink.pyflink
st_env.execute_sql("""
 CREATE TABLE impressions (
 bid_id VARCHAR,
 creative_details VARCHAR(10),
 campaign_id VARCHAR,
 country_code VARCHAR(5),
 i_timestamp VARCHAR,
 serve_time as TO_TIMESTAMP (`i_timestamp`, 'EEE MMM dd HH:mm:ss z yyyy'),
 WATERMARK FOR serve_time AS serve_time -INTERVAL '5' SECOND
 )
 WITH (
 'connector'= 'kafka',
 'topic' = 'impressions',
 'properties.bootstrap.servers' = '< Bootstrap Servers shown in the MSK client info dialog >',
 'format' = 'json',
 'properties.group.id' = 'testGroup1',
 'scan.startup.mode'= 'earliest-offset',
 'json.timestamp-format.standard'= 'ISO-8601'
 )""")
 
st_env.execute_sql("""
 CREATE TABLE clicks (
 correlation_id VARCHAR,
 tracker VARCHAR(100),
 c_timestamp VARCHAR,
 click_time as TO_TIMESTAMP (`c_timestamp`, 'EEE MMM dd HH:mm:ss z yyyy'),
 WATERMARK FOR click_time AS click_time -INTERVAL '5' SECOND
 )
 WITH (
 'connector'= 'kafka',
 'topic' = 'clicks',
 'properties.bootstrap.servers' = '< Bootstrap Servers shown in the MSK client info dialog >',
 'format' = 'json',
 'properties.group.id' = 'testGroup1',
 'scan.startup.mode'= 'earliest-offset',
 'json.timestamp-format.standard'= 'ISO-8601'
 )""")
```

## Stream - batch processing

```py
from pyflink.table import EnvironmentSettings, TableEnvironment

# in_streaming_mode() 와 in_batch_mode() 설정 
t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())
#t_env = TableEnvironment.create(EnvironmentSettings.in_batch_mode())

# 최대 병렬 처리 개수 
t_env.get_config().set("parallelism.default", "1")
```

### sorcue / sink table 생성 

```py

```




# test sensor data

- [AWS DOC Amazon Kinesis Data Analytics Studio 소개](https://aws.amazon.com/ko/blogs/korea/introducing-amazon-kinesis-data-analytics-studio-quickly-interact-with-streaming-data-using-sql-python-or-scala/)
- json 기반으로 연결 테스트 가능 ( kafka 는 설정 되어 있다는 전제 )

### 1. 신호 생성시 (python)

```py
import datetime
import json
import random
import boto3
import kafka
from time import sleep
from json import loads, dumps

STREAM_NAME = "my-input-stream"

def get_random_data():
    current_temperature = round(10 + random.random() * 170, 2)
    if current_temperature > 160:
        status = "ERROR"
    elif current_temperature > 140 or random.randrange(1, 100) > 80:
        status = random.choice(["WARNING","ERROR"])
    else:
        status = "OK"
    return {
        'sensor_id': random.randrange(1, 100),
        'current_temperature': current_temperature,
        'status': status,
        'event_time': datetime.datetime.now().isoformat()
    }


def send_data(stream_name):
    producer_test = kafka.KafkaProducer(
            bootstrap_servers='b-2.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092',
            request_timeout_ms  = 600 * 1000,
            max_block_ms = 600 * 1000, 
            value_serializer=lambda m: dumps(m).encode('utf-8')
        )
    
    while True:
        data = get_random_data()
        partition_key = str(data["sensor_id"])
        
        res_producer = producer_test.send('flink_test', data)
        producer_test.flush()
        
        sleep(1)
        
        # print(data)
        
        # kinesis_client.put_record(
        #     StreamName=stream_name,
        #     Data=json.dumps(data),
        #     PartitionKey=partition_key)


if __name__ == '__main__':
    # kinesis_client = boto3.client('kinesis')
    send_data(STREAM_NAME)
```


### flink table 생성
```python
%flink.ssql(type=update)
CREATE TABLE flink_test (
    sensor_id INTEGER,
    current_temperature DOUBLE,
    status VARCHAR(6),
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
)
PARTITIONED BY (sensor_id)
WITH (
'connector'= 'kafka',
'topic' = 'flink_test',
'properties.bootstrap.servers' = 'b-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092',
'format' = 'json',
'properties.group.id' = 'flink_consumer_group_11',
'json.timestamp-format.standard' = 'ISO-8601'
-- 'scan.startup.mode'= 'earliest-offset'
);
```

### avro test

```py
%flink.ssql(type=update)
CREATE TABLE flink_avro_gn_news_company_table (
    news_url_md5 CHAR(32),
    company_code VARCHAR(7),
    ncc_flag VARCHAR(1),
    use_flag VARCHAR(1),
    published_at VARCHAR(30)
)
PARTITIONED BY (company_code)
WITH (
'connector'= 'kafka',
'topic' = 'news.gn_news_company_table',
'properties.bootstrap.servers' = 'b-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092, b-6.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092, b-5.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092',
'value.format' = 'avro',
'properties.group.id' = 'flink_consumer_group_news_prod_01'
-- 'scan.startup.mode'= 'earliest-offset'
);
```


# 오류 사항 

- flink 1.14

- identifiers 오류
1. prod/flink/flink-avro-1.17-SNAPSHOT.jar 설치
2. prod/flink/flink-table-common-1.17-SNAPSHOT.jar  설치 
    - Caused by: java.util.ServiceConfigurationError: org.apache.flink.table.factories.Factory: org.apache.flink.table.module.CoreModuleFactory not a subtype 발생 
    - 
```bash
Caused by: org.apache.flink.table.api.ValidationException: Could not find any factory for identifier 'avro' that implements 'org.apache.flink.table.factories.DeserializationFormatFactory' in the classpath.

Available factory identifiers are:

canal-json
csv
debezium-json
json
maxwell-json
raw

```


- BulkReaderFormatFactory ( factory utils 오류 )
- flink-connector-files-1.17-SNAPSHOT.jar 해당 폴더의 하위 클래스에 해당 class 존재 확인 후 추가 

```bash
Caused by: java.lang.NoClassDefFoundError: org/apache/flink/connector/file/table/factories/BulkReaderFormatFactory
```



## flink 1.14 download

- https://github.com/apache/flink/tags

```bash

aws s3 cp flink-avro-1.14.6.jar  s3://aicel-workflow/prod/flink/1.14/

aws s3 cp flink-avro-glue-schema-registry-1.14.6.jar  s3://aicel-workflow/prod/flink/1.14/

aws s3 cp flink-sql-avro-1.14.6.jar  s3://aicel-workflow/prod/flink/1.11/

aws s3 cp avro-1.11.1.jar  s3://aicel-workflow/prod/flink/1.11/

aws s3 cp flink-avro-1.11.2.jar  s3://aicel-workflow/prod/flink/1.11/


```

- avro jar 파일 필요 
  
- [dwonload page](https://dlcdn.apache.org/avro/stable/java/)

```bash
Caused by: java.lang.ClassNoCaused by: java.lang.ClassNotFoundException: org.apache.avro.

Caused by: java.lang.ClassNotFoundException: org.apache.avro.generic.GenericData$Array



```

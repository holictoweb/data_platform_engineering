
MSK 크라이언트 설치 


## broker & zookeeper

```bash 
# broker IAM 
b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9098
b-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9098
b-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9098

# broker TLS
b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094
b-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094
b-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094

# plaintext
z-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:2181
z-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:2181
z-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:2181

# without TLS broker 
b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092
b-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092
b-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092



```




## topic 생성 

```bash
# 토픽 생성 
bin/kafka-topics.sh --create --zookeeper z-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:2181 --replication-factor 3 --partitions 1 --topic MSKStreams

# 토픽 리스트 확인
bin/kafka-topics.sh --list --zookeeper z-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:2181

# 토픽 상세 정보 
bin/kafka-topics.sh --describe --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --topic news.thebell.newslist

```




## producer
```bash
# 토픽 메세지  생성
# bin/kafka-console-producer.sh --broker-list b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094 --producer.config config/client.properties --topic MSKStreams

# bin/kafka-console-producer.sh --broker-list b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094 --producer.config config/client.properties --topic MSKStreams

# no TLS
bin/kafka-console-producer.sh --broker-list b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --producer.config config/client.properties --topic MSKStreams


bin/kafka-console-producer.sh --broker-list b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --producer.config config/client.properties --topic news.thebellpage
```

# consumer 
>- bootstrap.server : 카프카 클러스터에 처음 연결을 하기 위한 호스트와 포트 정보로 구성된 리스트 정보를 나타냅니다.
>- fetch.min.bytes : 한번에 가져올 수 있는 최소 데이터 사이즈입니다. 만약 지정한 사이즈보다 작은 경우, 데이터가 누적될 때까지 기다립니다.
>- group.id : 컨슈머가 속한 컨슈머 그룹을 식별하는 식별자입니다.
>- enable.auto.commit : 백그라운드로 주기적으로 오프셋을 커밋합니다.
>- auto.offset.reset : 카프카에서 초기 오프셋이 없거나 현재 오프셋이 더 이상 존재하지 않은 경우에 다음 옵션으로 리셋합니다.
>   - earliest : 가장 초기의 오프셋값으로 설정
>   - latest : 가장 마지막의 오프셋값으로 설정
>   - none : 이전 오프셋값을 찾이 못하면 에러
>- fetch.max.bytes : 한번에 가져올 수 있는 최대 데이터 사이즈
>- reques.timeout.ms : 요청에 대해 응답을 기다리는 최대 시간
>- session.timeout.ms : 컨슈머와ㅓ 브로커 사이의 세션 타임 아웃 시간. 브로커가 컨슈머가 살아있는것으로 판단하는 시간으로, 만약 컨슈머가 그룹 코디네이터에게 하트비트를 보내지 않고 시간이 지나면 해당 컨슈머는 종료되거나 장애가 발생한 것으로 판단하고 컨슈머 그룹은 리밸런스를 시도합니다.
heartbeat.interval.ms : 그룹 코디네이터에게 얼마나 자주 KafkaConsumer poll() 메소드로 하트비트를 보낼 것인지 조정
>- max.poll.records : 단일 호출 poll()에 대한 최대 레코드 수를 조정
>- max.poll.interval.ms : 컨슈머가 살아있는지를 체크하기 위해 하트비트를 주기적으로 보내는데, 컨슈머가 계속해서 하트비트만 보내고 실제로 메시지를 가져가지 않는 경우가 있을 수도 있습니다. 이러한 경우 컨슈머가 무한정 해당 파티션을 점유할 수 없도록 주기적으로 poll을 호출하지 않으면 장애라고 판단하고 컨슈머 그룹에서 제외한 후 다른 컨슈머가 해당 파티션에서 메시지를 가져갈 수 있게 합니다.
>- auto.commit.interval.ms 주기적으로 오프셋을 커밋하는 시간
>- fetch.max.wait.ms : fetch.min.bytes에 설정된 데이터보다 적은 경우 요청에 응답을 기다리는 최대 시간

## consumer
```bash
# 토픽 메세지 확인
bin/kafka-console-consumer.sh --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --consumer.config config/client.properties--topic MSKStreams --from-beginning

# client.config 를 사용 하지 않고 실행 - client.properties 파일을 찾지 못하는 오류 발생 
bin/kafka-console-consumer.sh --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --topic thebell-list --from-beginning

bin/kafka-console-consumer.sh --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --topic thebell-list

bin/kafka-console-consumer.sh --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --topic news.thebell.newspage

```

## consumer group 
- consumer 생성 시 consumer group 이 생성
- group_id를 통해 동일 consumert group 생성 가능. 
```bash 
# consumer 생성 시 group 지정
bin/kafka-console-consumer.sh \
--bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic news.thebell.newslist \
--group thebell-consumer-group \
--from-beginning



bin/kafka-console-consumer.sh \
--bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic news.thebell.newslist \
--group thebell-consumer-group


# consumer gropu 리스트
bin/kafka-consumer-groups.sh --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --list

# consumer group 상세 정보
bin/kafka-consumer-groups.sh  --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --group thebell-consumer-group --describe

# LAG 확인  ( current-ofsetm log-end-offset 의 차이 )
bin/kafka-consumer-group.sh --bootstrap-server b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092 --describe --group my-group


# client id 를 지정 하여 적용 가능?
```

## MSK CLI
```bash
# 클러스터 리스트 확인
aws kafka list-clusters

# brocker 확인 
aws kafka get-bootstrap-brokers --cluster-arn arn:aws:kafka:ap-northeast-2:445772965351:cluster/aicel-kafka-dev/04e8215e-c7e1-4977-838b-1c109cc44a48-2

# 결과 확인 
{
    "BootstrapBrokerStringTls": "b-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094,b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094,b-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9094",
    "BootstrapBrokerStringSaslScram": "b-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9096,b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9096,b-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9096",
    "BootstrapBrokerStringSaslIam": "b-1.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9098,b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9098,b-3.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9098"
}


```


# CLI를 통한 클러스터 생성 ( encryption )

1. 암호화 관련 설정 파일 생성 
```json

{
   "EncryptionAtRest": {
       "DataVolumeKMSKeyId": "arn:aws:kms:ap-northeast-2:445772965351:key/48aacbe2-b8e8-4f5c-9d2e-af86346aee16"
    },
   "EncryptionInTransit": {
        "InCluster": true,
        "ClientBroker": "TLS"
    }
}
```

2. 클러스터 생성 
```bash
aws kafka create-cluster --cluster-name "ExampleClusterName" --broker-node-group-info file://brokernodegroupinfo.json --encryption-info file://encryptioninfo.json --kafka-version "2.6.2" --number-of-broker-nodes 3
```






# MSK public access 연결 허용

```

aws kafka update-connectivity --cluster-arn ClusterArn --current-version Current-Cluster-Version --connectivity-info '{"PublicAccess": {"Type": "SERVICE_PROVIDED_EIPS"}}'


```




# 연결 오류
- https://aws.amazon.com/ko/premiumsupport/knowledge-center/msk-connector-connect-errors/





# MSK connect
- connector 생성 가이드
- https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect-connectors.html

## debezium connector ( sink로 사용 가능한지는 확인이 필요)
- 기본적으로 플러그인을 먼저 s3에 올린 후 등록 
- msk > connector > custom plugin > 
- https://catalog.us-east-1.prod.workshops.aws/workshops/c2b72b6f-666b-4596-b8bc-bafa5dcca741/en-US/mskconnect/source-connector-setup
```bash
mkdir debezium && cd debezium
wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-mysql/1.7.0.Final/debezium-connector-mysql-1.7.0.Final-plugin.tar.gz

tar xzf debezium-connector-mysql-1.7.0.Final-plugin.tar.gz

cd debezium-connector-mysql

zip -9 ../debezium-connector-mysql-1.7.0.Final-plugin.zip *

cd ..
aws s3 cp ./debezium-connector-mysql-1.7.0.Final-plugin.zip s3://oss-packages/dev/debezium/

```
### 

## jdbc connector


```py
connector.class=io.confluent.connect.jdbc.JdbcSinkConnector
transforms.TimestampConverter.target.type=Timestamp
table.name.format=test.test_table
connection.password=12345
transforms.TimestampConverter.field=DATE
tasks.max=1
topics=kafka_test
transforms.TimestampConverter.type=org.apache.kafka.connect.transforms.TimestampConverter$Value
transforms=TimestampConverter
transforms.TimestampConverter.format=yyyy-MM-dd HH:mm:ss
auto.evolve=false
connection.user=dbuser
auto.create=false
connection.url=jdbc:mysql://Targetdb:3306:test
insert.mode=insert

```


connection.url="jdbc:mysql://127.0.0.1:3306/sample?verifyServerCertificate=false&useSSL=true&requireSSL=true"

### kafka release note
https://kafka.apache.org/downloads



```bash

# 현재 최신 버젼 3.2.0
wget https://archive.apache.org/dist/kafka/3.1.1/kafka_2.13-3.1.1.tgz

# 압축 해제
tar -zxvf kafka_2.13-3.1.1.tgz

# connect는 함께 설치
```


# 실행
- 주키퍼, 카프카, connect 실행 
- kafka 디렉토리 상에서 실행 

```bash
# 주키퍼 실행 
bin/zookeeper-server-start.sh config/zookeeper.properties

# 카프카 실행 
bin/kafka-server-start.sh config/server.properties

# connect 실행
# connect-distributed.properties 변경 -> bootstrap.servers=10.0.2.127:9092
# 카프카 브로커 서버의 listerner 에 등록된 내용으로 변경 
bin/connect-distributed.sh config/connect-distributed.properties
# standalone 실행 
bin/connect-standalone.sh config/connect-standalone.properties config/connect-
# connct가 살아 있는지 확인
curl -s localhost:8083

```





# topic 생성
- 생성 시 각각의 .properties 파일의 설정을 바꾸고 진행 하는것이 나음. 
```bash
# 토픽 생성 
bin/kafka-topics.sh --create --topic news-nlp --bootstrap-server 10.0.2.127:9092

# 토픽 list 확인
bin/kafka-topics.sh --list --bootstrap-server 10.0.2.127:9092

# 토픽 설정 확인
bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server 10.0.2.127:9092



```

# 메세지 생성
```bash
# producer 
bin/kafka-console-producer.sh --broker-list 10.0.2.127:9092 --topic news-nlp

# consumer
bin/kafka-console-consumer.sh --bootstrap-server 10.0.2.127:9092 --topic news-nlp --from-beginning
```










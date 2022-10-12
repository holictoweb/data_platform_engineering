https://docs.aws.amazon.com/ko_kr/msk/latest/developerguide/create-topic.html

- sudo yum install java-1.8.0
- wget https://archive.apache.org/dist/kafka/2.6.2/kafka_2.12-2.6.2.tgz

위 버젼으로 일단 시작 필요 상하위 호환에 대한 부분은 확인 못했지만 일단 동일 버젼으로 클라이언트 머신 생성 필요 

# 운영 환경 
```bash
b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092,b-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092,b-2.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092

# 운영 서버 
b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092
b-2.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092
b-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092


z-2.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181,z-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181,z-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181

# zookeeper 주소
z-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181
z-2.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181
z-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181

```

# create topic

```bash

bin/kafka-topics.sh --create \
--zookeeper z-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181 \
--replication-factor 2 --partitions 3 --topic droom.naver.meta

# 토픽 리스트 확인
bin/kafka-topics.sh --list \
--zookeeper z-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181


bin/kafka-topics.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--describe \
--topic droom.naver.start_requests


```

# change topic

```bash
# topic partition 변경 
bin/kafka-topics.sh \
--zookeeper z-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:2181 \
--alter --topic droom.naver.pipeline.meta \
--partitions 20

# retention 기간 변경
bin/kafka-configs.sh --bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--entity-type topics \
--entity-name droom.naver.start_requests \
--alter --add-config retention.ms=600000



```

# producer 
```bash
# plain text
bin/kafka-console-producer.sh \
--broker-list b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--producer.config config/client.properties \
--topic news.thebellpage

bin/kafka-console-producer.sh \
--broker-list b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic droom.naver.meta


```


# consumer 
```bash
# post
bin/kafka-console-consumer.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--from-beginning \
--topic droom.naver.meta 


# meta
bin/kafka-console-consumer.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--from-beginning \
--topic droom.naver.meta 


bin/kafka-console-consumer.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic droom.naver.start_requests 


# company
bin/kafka-console-consumer.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic news.naver.gn_news_company_table

# crawl_list
bin/kafka-console-consumer.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic droom.naver.pipeline.crawl_list

bin/kafka-console-consumer.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--topic droom.naver.pipeline.meta



```

# consumer group 확인
```bash
# consumer group list 
bin/kafka-consumer-groups.sh  --list --bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092

# consumer group describe
bin/kafka-consumer-groups.sh --describe \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--group droom_meta_scrapy_consumer_group


# meta
bin/kafka-consumer-groups.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--describe \
--group droom_meta_scrapy_consumer_group 

# post
bin/kafka-consumer-groups.sh \
--bootstrap-server b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--describe \
--group droom_post_scrapy_consumer_group 


```



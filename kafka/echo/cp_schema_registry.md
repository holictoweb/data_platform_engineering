


# local schema registry 시작
```bash
# properties 상의 bootstrap 정보 변경 
# /home/ubuntu/confluent/confluent-7.3.0/etc/schema-registry/schema-registry.properties
listeners=http://0.0.0.0:8082
kafkastore.bootstrap.servers=PLAINTEXT://b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092
kafkastore.topic=_schemas

# 실행 
bin/schema-registry-start etc/schema-registry/schema-registry.properties

```


# 기본 api
## schema 정보 확인

```bash

curl -X GET http://localhost:8081/subjects

# config 확인
curl -X GET http://localhost:8081/config

```



# API 

```
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"schema": "{\"type\": \"string\"}"}' \
  http://localhost:8082/subjects/Kafka-key/versions

curl -X GET http://localhost:8082/subjects

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"schema": "{\"type\": \"string\"}"}' \
  http://localhost:8082/subjects/aicel-news-schema/versions
```


# confluent-python 사용 조회 
```bash
pip install confluent-kafka
```

## 조회 및 생성 
```py

from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
from pprint import pprint

sr = CachedSchemaRegistryClient({
    'url': 'http://localhost:8082'
})

value_schema = sr.get_latest_schema("aicel-news-schema")[1]
# key_schema= sr.get_latest_schema("orders-key")[1]
```

## kafka produecer 


## kafka consumer

```bash
kafka-avro-console-consumer --bootstrap-server kafka-all-broker:29092 --topic users --from-beginning --property schema.registry.url=http://schema-registry-svc-kafka.kafka.svc.cluster.local:8081
```




# confluent kafka python with schema registry


```py

```
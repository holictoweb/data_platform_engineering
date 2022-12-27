

# confluent_kafka python api
[confluent_kafka API 공식 문서](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-consumer)

[confluent python example](https://github.com/confluentinc/confluent-kafka-python/tree/master/examples)


# kafka connect
[working with sasl_ssl ](https://github.com/edenhill/librdkafka/issues/2526)
```py

```


## create topic
```py
from confluent_kafka.admin import AdminClient, NewTopic
from pprint import pprint

admin_client = AdminClient({
    "bootstrap.servers": "localhost:9092"
})

topic_list = []
topic_list.append(NewTopic("example_topic", 1, 1))
admin_client.create_topics(topic_list)

# topic list
list = admin_client.list_topics().topics
pprint(list)

```





# pro sub

### produce
```py
from confluent_kafka.schema_registry import SchemaRegistryClient
from pprint import pprint
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka import Producer, Consumer
import numpy as np
from time import sleep
import json
import random
import string

sr_client_conf = {  
    'url': 'http://internal-a99ee70ba73e64da5ae88b3ced546d98-1542137584.ap-northeast-2.elb.amazonaws.com:8083'
}
sr_client = SchemaRegistryClient(sr_client_conf)


prod_conf = {'bootstrap.servers': 'b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092'}
p = Producer(prod_conf)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

idx = 0
while True :
    numeric = np.random.normal(loc = 10 , scale = 20 ,size= 100).astype(str).tolist()
    numerics = ",".join( numeric )
    data = ''.join(random.choice(string.ascii_letters) for i in range(32))
    message = {
        "radom_string": data,
        "radom_numeric": numerics
    }

    p.poll(0)
    p.produce('news.lji.test', json.dumps(message).encode('utf-8'), callback=delivery_report)
    sleep(2.0)
    if idx % 100 == 0 :
        input("hi")
    idx += 1 
# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()

```


# schema registry

```py
from confluent_kafka.schema_registry import SchemaRegistryClient
from pprint import pprint 
from json import dumps

SCHEMA_HOST = "172.31.115.111:31001"
SUBJECT_NAME = "foreign-exchange-rate-value"

schema_registry_conf = {'url': "http://{}".format(SCHEMA_HOST)}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

schema = schema_registry_client.get_latest_version(subject_name=SUBJECT_NAME)

schema = schema_registry_client.get_schema(schema.schema_id)
schema_str = schema.schema_str

pprint(schema_str)
```


faust-streamming

https://github.com/faust-streaming/faust



# streams 
```py
import faust 


app = faust.App('hit_counter',broker="kafka://localhost:29092")


```


![](https://cdn.confluent.io/wp-content/uploads/integrations-with-apache-kafka-768x503.png)






# python api
- kafka-python
```bash
pip install kafka-python
```

## boto3 get broker list

```py
import boto3
from pprint import pprint
import pandas as pd

cluser_name = 'aicel-kafka-prod'


msk_client = boto3.client('kafka', region_name='ap-northeast-2')
response = msk_client.list_clusters(
    # ClusterNameFilter='string',
    # MaxResults=123,
    # NextToken='string'
)
df = pd.DataFrame(response['ClusterInfoList'])
# pprint(response)
cluster_arn = df.loc[df.ClusterName == cluser_name, 'ClusterArn'].item()

print(f"*** Target cluser {cluser_name} Arn: {cluster_arn}")

response = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
bootstrap_list = response['BootstrapBrokerString'].split(',')

print(f"*** Target bootstrap : {bootstrap_list}")

```

##  topic list 

```py
import boto3
from pprint import pprint
import pandas as pd
import kafka
from kafka.admin import KafkaAdminClient, NewTopic
import pandas as pd

cluser_name = 'aicel-kafka-prod'


msk_client = boto3.client('kafka', region_name='ap-northeast-2')
response = msk_client.list_clusters(
    # ClusterNameFilter='string',
    # MaxResults=123,
    # NextToken='string'
)
df = pd.DataFrame(response['ClusterInfoList'])
# pprint(response)
cluster_arn = df.loc[df.ClusterName == cluser_name, 'ClusterArn'].item()

print(f"*** Target cluser {cluser_name} Arn: {cluster_arn}")


response = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
bootstrap_list = response['BootstrapBrokerString'].split(',')

print(f"*** Target bootstrap : {bootstrap_list}")

consumer = kafka.KafkaConsumer( bootstrap_servers=bootstrap_list)
topic_list = list(consumer.topics())
# print(type(topic_list))
pprint(topic_list)
```

## create topic

```py

from kafka.admin import KafkaAdminClient, NewTopic


admin_client = KafkaAdminClient(
    bootstrap_servers="b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092", 
    client_id='test'
)

topic_list = []
topic_list.append(NewTopic(name="example_topic", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)


```  

## delete topic

```py
from kafka.admin import KafkaAdminClient, NewTopic


admin_client = KafkaAdminClient(
    bootstrap_servers="b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092"
)
topic_names = 'greetings'
admin_client.delete_topics(topics=topic_names)
```

# topic 생성 소비

## producer

```py

# message generator

import random 
import string 

user_ids = list(range(1, 101))
recipient_ids = list(range(1, 101))

def generate_message() -> dict:
    random_user_id = random.choice(user_ids)
    # Copy the recipients array
    recipient_ids_copy = recipient_ids.copy()
    # User can't send message to himself
    recipient_ids_copy.remove(random_user_id)
    random_recipient_id = random.choice(recipient_ids_copy)
    # Generate a random message
    message = ''.join(random.choice(string.ascii_letters) for i in range(32))
    return {
        'user_id': random_user_id,
        'recipient_id': random_recipient_id,
        'message': message
    }



# Kafka Producer
from kafka import KafkaProducer
import json

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092'],
    value_serializer=serializer
)

dummy_message = generate_message()
print(dummy_message)

producer.send('MSKStreams', dummy_message)
producer.close()

```

## consumer 

- 연결 후 들어 오는 데이터만 바로 보고 있는 부분은 어떻게 해결 해야 할지 offset 관리에 대한 부분 확인 필요 
```py
import kafka
from json import loads

consumer = kafka.KafkaConsumer(
    'MSKStreams',
    bootstrap_servers=['b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092'],
    # auto_offset_reset='earliest',
    #  enable_auto_commit=True,
    #  value_deserializer=lambda x: loads(x.decode('utf-8')),
    #  consumer_timeout_ms=1000
)
for msg in consumer:
  recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
  print(recv)
```



- - -
<br>
<br>
<br>

# Faust 사용 stream api 
- git : https://github.com/faust-streaming/faust

- hello world
- 실행은 faust 명령을 통해 진행
  - faust -A hello_world send @greet "Hello Faust"
  - topic 은 미리 생성 필요 
```py
import faust

app = faust.App(
    'hello-world',
    broker='kafka://b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092',
    value_serializer='raw',  # test를 위해 raw 사용 
)


greetings_topic = app.topic('greetings')

@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)
```






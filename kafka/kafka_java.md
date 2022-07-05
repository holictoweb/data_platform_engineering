
# Streams api DSL
- https://kafka.apache.org/20/documentation/streams/developer-guide/dsl-api.html#:~:text=The%20Kafka%20Streams%20DSL%20(Domain,few%20lines%20of%20DSL%20code.

## 주요 문법 
```java

```

## json data 처리
- https://medium.com/@agvillamizar/implementing-custom-serdes-for-java-objects-using-json-serializer-and-deserializer-in-kafka-streams-d794b66e7c03
- json 메세지에 대한 처리 방법 
```java
```


# java api 

## producer 
```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import java.util.Properties;


public class Firstproducer {

    public static void main(String[] args){
        Properties props = new Properties();
        props.put("bootstrap.servers", "b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        Producer<String, String> producer = new KafkaProducer<>(props);
        try{
            producer.send(new ProducerRecord<String, String>("greetings","whole new world"));
            producer.send(new ProducerRecord<String, String>("greetings","IU whole"));
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            producer.close();
        }
    }
}

```

# Streams api 
- 기본적으로 단순 흐름을 만드는 streams api 
```java

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;

import org.apache.kafka.streams.kstream.KStream;



import java.util.Properties;
import java.util.concurrent.CountDownLatch;




public class Pipe {

    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

        final StreamsBuilder builder = new StreamsBuilder(); // 프로세서 토폴로지를 구성하는데 사용하는 Streambuilder 인스턴스 생성 

        // 단순 이동 
        // builder.stream("streams-source").to("streams-sink");
        builder.stream("streams-source").to("streams-sink");

        
        final Topology topology = builder.build();

        System.out.println(topology.describe());

        final KafkaStreams streams = new KafkaStreams(topology, props);
        final CountDownLatch latch = new CountDownLatch(1);
        
        // Ctrl+C를 처리하기 위한 핸들러 추가
        Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
                System.out.println("topology terminated");
            }
        });

        try {
            streams.start(); // 스트림 시작 
            System.out.println("topology started");
            latch.await();
        } catch (Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }
}


```

## uppercase 변환

```java

public class Pipe_transform {
    private static String TOPIC_SOURCE = "streams-source";
    private static String TOPIC_SINK = "streams-sink";

    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "b-2.aicelkafkadev.b3c0a9.c2.kafka.ap-northeast-2.amazonaws.com:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        
        final StreamsBuilder builder = new StreamsBuilder(); 

        KStream<String, String> wordCount = builder.stream(TOPIC_SOURCE);
        KStream<String, String> filteredStream = wordCount.filter(
            // new Predicate<String,String>() {
            //     @Override
            //     public boolean test(String key, String value) {
            //             System.out.println("Key : '" + key + "'', value : '" + value + "'");
            //             return value.length() > 15;
            //     }
            // }
                (key, value) -> {
                    System.out.println("Key : '" + key + "'', value : '" + value + "'");
                    return value.length() > 15;
                }
        );
        KStream<String, String> mapedStream = filteredStream.mapValues(text -> text.toUpperCase());
        mapedStream.to(TOPIC_SINK);

        KafkaStreams streams = new KafkaStreams(builder.build(), props);

        final CountDownLatch latch = new CountDownLatch(1);
        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread("streams-wordcount-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
            }
        });

        try {
            System.out.println("this is Pipe_transform ----------------------------------------------------------");

            streams.start();
            System.out.println("Stream started ----------------------------------------------------------");
            latch.await();
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
}
```







https://search.naver.com/search.naver?where=news&query=기아&sort=1&pd=9





https://n.news.naver.com/mnews/article/011/0004066801
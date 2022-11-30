# kafka 관리툴 


## kafka-ui 사용

- [github](https://github.com/provectus/kafka-ui)

### docker lunch

```bash
docker run -p 8080:8080 \
	-e KAFKA_CLUSTERS_0_NAME=aicel-kafka-prod \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
	-d provectuslabs/kafka-ui:latest

```
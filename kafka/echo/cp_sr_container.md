# confluent helm
```bash
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
"confluentinc" has been added to your repositories


```


# confluent 

```bash
docker run -p 8083:8083  \
  --name=aicel-schema-registry \
  -e SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS=b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
  -e SCHEMA_REGISTRY_HOST_NAME=localhost \
  -e SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8083 \
  -e SCHEMA_REGISTRY_DEBUG=true \
  -d confluentinc/cp-schema-registry:7.3.0
```
  
```bash
docker run -p 8083:8083  \
  --name=aicel-schema-registry \
  -e SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
  -e SCHEMA_REGISTRY_HOST_NAME=localhost \
  -e SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8083 \
  -e SCHEMA_REGISTRY_DEBUG=true \
  -d confluentinc/cp-schema-registry:7.3.0

# ecr 
docker run -p 8083:8083  \
  --name=aicel-schema-registry \
  -e SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9098 \
  -e SCHEMA_REGISTRY_HOST_NAME=localhost \
  -e SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8083 \
  -e SCHEMA_REGISTRY_DEBUG=true \
  -d 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/aicel-schema-registry:dev-schema-registry
```


```bash
docker run -it --net=host --rm confluentinc/cp-schema-registry:7.3.0 bash

```


docker run -p 9090:8080 \
	-e KAFKA_CLUSTERS_0_NAME=aicel-msk-dev \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
	-d provectuslabs/kafka-ui:latest 





# kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: schema-registry-test
  name: aicel-schema-registry-v2
  labels:
    app: aicel-schema-registry-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aicel-schema-registry-v2
  template:
    metadata:
      labels:
        app: aicel-schema-registry-v2
    spec:
      containers:
      - env:
        - name: SCHEMA_REGISTRY_HOST_NAME
          value: aicel-schema-registry-v2
        - name: SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS
          value: PLAINTEXT://b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092
        - name: SCHEMA_REGISTRY_LISTENERS
          value: http://0.0.0.0:8083
        name: aicel-schema-registry-v2
        image: confluentinc/cp-schema-registry:7.3.0
        imagePullPolicy: Always
        ports:
        - containerPort: 8083
          protocol: TCP

Service:
apiVersion: v1
kind: Service
metadata:
  annotations: 
    service.beta.kubernetes.io/aws-load-balancer-internal: 0.0.0.0/0
  name: aicel-schema-registry-v2
  namespace: schema-registry-test
  labels:
    app: aicel-schema-registry-v2
spec:
  selector:
    app: aicel-schema-registry-v2
  ports:
  - port: 8083
  type: LoadBalancer
```

```conf
# Inject AWS IAM Auth to Confluent image
FROM confluentinc/cp-schema-registry:7.2.2

USER root
ADD --chown=appuser:appuser https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.4/aws-msk-iam-auth-1.1.4-all.jar /usr/share/java/cp-base-new/
ADD --chown=appuser:appuser https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.4/aws-msk-iam-auth-1.1.4-all.jar /usr/share/java/schema-registry/

ENV SCHEMA_REGISTRY_KAFKASTORE_SECURITY_PROTOCOL="SASL_SSL"
ENV SCHEMA_REGISTRY_KAFKASTORE_SASL_MECHANISM="AWS_MSK_IAM"
ENV SCHEMA_REGISTRY_KAFKASTORE_SASL_JAAS_CONFIG="software.amazon.msk.auth.iam.IAMLoginModule required;"
ENV SCHEMA_REGISTRY_KAFKASTORE_SASL_CLIENT_CALLBACK_HANDLER_CLASS="software.amazon.msk.auth.iam.IAMClientCallbackHandler"

USER appuser
```



software.amazon.msk.auth.iam.IAMLoginModule required awsProfileName="arn:aws:iam::445772965351:role/aicel-developer-kafka-service-local";
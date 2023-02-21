
# helm chart
[kafka ui helm 개발 가이드](https://github.com/provectus/kafka-ui/blob/master/helm_chart.md)
```bash
helm repo add kafka-ui https://provectus.github.io/kafka-ui

# check chart version
helm search repo kafka-ui

# helm chart download
helm pull kafka-ui/kafka-ui --version 0.4.5 --insecure-skip-tls-verify

helm pull kafka-ui/kafka-ui --version 0.4.5 --insecure-skip-tls-verify

helm pull prefect/prefect-orion --version 2.7.1 --insecure-skip-tls-verify

helm install kafka-ui kafka-ui/kafka-ui \
--version 0.4.5 \
--namespace kafka-group \
--set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 


helm install kafka-ui kafka-ui/kafka-ui \
--version 0.4.5 \
--namespace kafka-group \
--set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 



# 1. 계정 생성의 경우 먼저 생성 후 iamservice account 설정 필요 ( heml 생성 시 eksctl로 연결 생성된 계정에 대한 override가 안되는 것으로 보임. )
eksctl create iamserviceaccount --name sa-kafka-ui \
--namespace kafka-group \
--cluster aicel-elt-pipeline-prd \
--attach-policy-arn arn:aws:iam::445772965351:policy/AmazonMSK-aicel-kafka-prd-rw \
--approve \
--override-existing-serviceaccounts \
--role-name eksctl-serviceaccount-kafka-ui-prd

# 생성된 account 확인
eksctl get iamserviceaccount --cluster aicel-elt-pipeline-dev --namespace kafka-group

#### install plaintext
helm install kafka-ui-plain . \
	--namespace kafka-group \
    --set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kakfa-dev-plain \
    --set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092

helm upgrade kafka-ui-plain . \
    --set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kakfa-dev-plain \
    --set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092

#### install iam_auth
helm install  kafka-ui-init . \
--namespace kafka-group \
--set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-1.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9098 \
--set envs.config.KAFKA_CLUSTERS_0_PROPERTIES_SECURITY_PROTOCOL=SASL_SSL \
--set envs.config.KAFKA_CLUSTERS_0_PROPERTIES_SASL_MECHANISM=AWS_MSK_IAM \
--set envs.config.KAFKA_CLUSTERS_0_PROPERTIES_SASL_CLIENT_CALLBACK_HANDLER_CLASS=software.amazon.msk.auth.iam.IAMClientCallbackHandler \
--set envs.config.KAFKA_CLUSTERS_0_PROPERTIES_SASL_JAAS_CONFIG=software.amazon.msk.auth.iam.IAMLoginModule required; awsProfileName=""; \
--dry-run

# values.yaml
envs:
  secret: {}
  config: {
    KAFKA_CLUSTERS_0_NAME: aicel-kafka-dev,
    KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9098,
    KAFKA_CLUSTERS_0_PROPERTIES_SECURITY_PROTOCOL: SASL_SSL,
    KAFKA_CLUSTERS_0_PROPERTIES_SASL_MECHANISM: AWS_MSK_IAM, 
    KAFKA_CLUSTERS_0_PROPERTIES_SASL_CLIENT_CALLBACK_HANDLER_CLASS: software.amazon.msk.auth.iam.IAMClientCallbackHandler,
    KAFKA_CLUSTERS_0_PROPERTIES_SASL_JAAS_CONFIG: software.amazon.msk.auth.iam.IAMLoginModule required;,
  }

# ------------------  download 한 chart 을 통해 deploy
helm install aicel-kafka-ui . --namespace kafka-group 

helm install aicel-prefect . --namespace workflow 

helm upgrade -f values.prd.yaml aicel-kafka-ui . -n kafka-group


## test config file 
helm upgrade kafka-ui-init . \
--namespace kafka-group \
--set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-1.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9098 \

# pod의 환경 변수 확인 
- https://coldcode.tistory.com/2
kubectl -n kafka-group exec pod/kafka-ui-init-5849b668cf-frb8h printenv | grep AWS

# pod 에 shell 접근 
kubectl exec --stdin --tty pod/kafka-ui-init-5849b668cf-frb8h -- bin/bash




```



# helm chart 를 이용한 배포


```yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-ui-helm-values
data:
  KAFKA_CLUSTERS_0_NAME: "aicel-kafka-dev"
  KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: "b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092"
  AUTH_TYPE: "DISABLED"
  MANAGEMENT_HEALTH_LDAP_ENABLED: "FALSE" 


```




- - -

## prod
- 현재 적용 dev
```bash

docker run -p 9991:8080  \
	-e KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
	-e KAFKA_CLUSTERS_0_SCHEMAREGISTRY=http://internal-a9f93f44f3a8c4dec96f3e9b067055e0-815294924.ap-northeast-2.elb.amazonaws.com:8081 \
	-d provectuslabs/kafka-ui:latest 


```
- github https://github.com/provectus/kafka-ui
```bash
docker run -p 9991:8080 \
	-e KAFKA_CLUSTERS_0_NAME=aicel-msk-prod \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9098 \
	-d provectuslabs/kafka-ui:latest 

```

```bash
docker run -p 9991:8080  \
	-e KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9098 \
	-e KAFKA_CLUSTERS_0_SCHEMAREGISTRY=http://internal-a9f93f44f3a8c4dec96f3e9b067055e0-815294924.ap-northeast-2.elb.amazonaws.com:8081 \
	-d provectuslabs/kafka-ui:latest 

docker run -p 9099:8080  \
	-e KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
	-e KAFKA_CLUSTERS_0_SCHEMAREGISTRY=http://internal-a9f93f44f3a8c4dec96f3e9b067055e0-815294924.ap-northeast-2.elb.amazonaws.com:8081 \
	-d provectuslabs/kafka-ui:latest 


docker run -p 9991:8080  \
	-e KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9098 \
	-e KAFKA_CLUSTERS_0_PROPERTIES_SECURITY_PROTOCOL=SASL_SSL \
	-e KAFKA_CLUSTERS_0_PROPERTIES_SASL_MECHANISM=AWS_MSK_IAM \
	-e KAFKA_CLUSTERS_0_PROPERTIES_SASL_CLIENT_CALLBACK_HANDLER_CLASS=software.amazon.msk.auth.iam.IAMClientCallbackHandler \
	-e KAFKA_CLUSTERS_0_PROPERTIES_SASL_JAAS_CONFIG=software.amazon.msk.auth.iam.IAMLoginModule required; \
	-d provectuslabs/kafka-ui:latest 

# helm chart로 올리기
helm install kafka-ui kafka-ui/kafka-ui --set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev --set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 --set envs.config.KAFKA_CLUSTERS_0_SCHEMAREGISTRY=http://internal-a9f93f44f3a8c4dec96f3e9b067055e0-815294924.ap-northeast-2.elb.amazonaws.com:8081

```



# provectus/kafka-ui

```bash

docker run -p 8080:8080 \
    -e KAFKA_CLUSTERS_0_NAME=local \
    -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=<KAFKA_URL> \
    -e KAFKA_CLUSTERS_0_PROPERTIES_SECURITY_PROTOCOL=SASL_SSL \
    -e KAFKA_CLUSTERS_0_PROPERTIES_SASL_MECHANISM=AWS_MSK_IAM \
    -e KAFKA_CLUSTERS_0_PROPERTIES_SASL_CLIENT_CALLBACK_HANDLER_CLASS=software.amazon.msk.auth.iam.IAMClientCallbackHandler \
    -e KAFKA_CLUSTERS_0_PROPERTIES_SASL_JAAS_CONFIG=software.amazon.msk.auth.iam.IAMLoginModule required awsProfileName="aicel-dev-eks-assume-role-kafka"; \
    -d provectuslabs/kafka-ui:latest 
	
```
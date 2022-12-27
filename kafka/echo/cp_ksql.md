
# serviceaccount 가 실제 서비스에 영향이 있는가. 

```bash
eksctl create iamserviceaccount --name sa-ksql-server \
--namespace kafka-group \
--cluster aicel-elt-pipeline-dev \
--attach-policy-arn arn:aws:iam::445772965351:policy/AmazonMSK-aicel-kafka-dev-rw \
--approve \
--override-existing-serviceaccounts \
--role-name eksctl-serviceaccount-ksql-server

```

```bash
# cp-ksql-server 폴더 에서 실행 
helm install aicel-cp-ksql-server . --namespace kafka-group

# 환경 변수 확인 
kubectl -n kafka-group exec pod/aicel-cp-ksql-server-79565c5c6b-xsk2q printenv 
# shell 연결
kubectl exec --stdin --tty pod/aicel-cp-ksql-cp-ksql-server-578ff7f8f5-9pxds -- sh
```



# container 
- iam 모듈을 설치할 장소 확인 필요 아래 구조로 /usr/share/java/ksqldb-server 아래로 모듈 복사 
- *** confluent-common  confluent-hub-client  confluent-security  confluent-telemetry  cp-base-new  ksqldb-server  schema-registry ***
```bash
FROM confluentinc/cp-ksqldb-server:6.1.0

USER root
ADD --chown=appuser:appuser https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.4/aws-msk-iam-auth-1.1.4-all.jar /usr/share/java/cp-base-new/
ADD --chown=appuser:appuser https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.4/aws-msk-iam-auth-1.1.4-all.jar /usr/share/java/ksqldb-server/

# confluent doc 
# https://docs.ksqldb.io/en/latest/operate-and-deploy/installation/server-config/security/
ENV KSQL_SECURITY_PROTOCOL="SASL_SSL"
ENV KSQL_SASL_MECHANISM="AWS_MSK_IAM"
ENV KSQL_SASL_JAAS_CONFIG="software.amazon.msk.auth.iam.IAMLoginModule required;"
ENV KSQL_SASL_CLIENT_CALLBACK_HANDLER_CLASS="software.amazon.msk.auth.iam.IAMClientCallbackHandler"

USER appuser

```

# ksql CLI install
```bash

```

# basic 
[ksql syntax 5.3.0](https://docs.confluent.io/5.2.0/ksql/docs/developer-guide/syntax-reference.html)
```sql
-- table 조회 


```
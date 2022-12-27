

# openid provider는 클러스터당 한개이며 기본적으로 cluster 생성시 생성 

```bash 

https://oidc.eks.ap-northeast-2.amazonaws.com/id/0B3B47447D399224A043BDB568FDF6CD
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
 name: sa-aicel-schema-registry
 namespace: schema-registry-test
 attachRoleARN: arn:aws:iam::445772965351:role/aicel-workflow-role
```

- eksctl 을 사용하여 role과 연결
- [IAM 역할을 맡도록 kubernetes 서비스 계정 구성](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html#irsa-create-role)
```sh
# TEST

eksctl create iamserviceaccount \
    --name iam-test-sa \
    --namespace schema-registry-test \
    --cluster dev-cluster-v1 \
    --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
    --approve \
    --override-existing-serviceaccounts



eksctl create iamserviceaccount --name sa-aicel-schema-registry-role-connect \
--namespace schema-registry-test \
--cluster dev-cluster-v1 \
--role-name "aicel-workflow-kakfa-role" \
--attach-policy-arn arn:aws:iam::445772965351:policy/AmazonMSK-aicel-kafka-dev-rw \
--approve \
--override-existing-serviceaccounts

# role
eksctl create iamserviceaccount --name sa-schema-registry \
--namespace kafka-group \
--cluster aicel-elt-pipeline-dev \
--attach-role-arn arn:aws:iam::445772965351:role/eks-serviceaccount-kafka \
--approve \
--override-existing-serviceaccounts

# policy 를 통해 생성한 role 을 기반으로 확인 필요 
eksctl create iamserviceaccount --name sa-kafka-ui \
--namespace kafka-group \
--cluster aicel-elt-pipeline-dev \
--attach-policy-arn arn:aws:iam::445772965351:policy/AmazonMSK-aicel-kafka-dev-rw \
--approve \
--override-existing-serviceaccounts \
--role-name eksctl-serviceaccount-kafka-ui



eksctl create iamserviceaccount --cluster=<clusterName> --name=<serviceAccountName> --namespace=<serviceAccountNamespace> --attach-policy-arn=<policyARN> \ 
    --tags "Owner=John Doe,Team=Some Team"



# --cluster=<clusterName> --name=<serviceAccountName> --role-name "custom-role-name"

```

## yaml 파일로 생성
```bash
eksctl create iamserviceaccount --config-file=schema-registry.yaml

```
- yaml 파일 설정  
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: dev-cluster-v1
  region: ap-northeast

iam:
  withOIDC: true
  serviceAccounts:
  - metadata:
      name: sa-schema-registry
      # if no namespace is set, "default" will be used;
      # the namespace will be created if it doesn't exist already
      namespace: schema-registry-test
    attach-role-arn:
    - "arn:aws:iam::445772965351:role/aicel-workflow-role"
    tags:
      Env: "DEV"
      Team: "Data"

```


# eksctl 을 사용안하는 경우
- eksctl로 eksctl create iamserviceaccount 를 사용하기 위해서는 cloudformation등 권한이 필요 하여 일단 수작업 진행
- 기존 role과 연동 하기 위한 부분도 
## Install helm 
[install helm](https://helm.sh/ko/docs/intro/install/)
```bash
# https://github.com/helm/helm/releases
# download and install 의 url 확인 linux amd64
wget https://get.helm.sh/helm-v3.10.3-linux-amd64.tar.gz

# 압축 해제 하면 linux-amd64 형태로 파일 생성
tar -zxvf helm-v3.10.3-linux-amd64.tar.gz

# bin 폴더로 이동 
mv linux-amd64/helm /usr/local/bin/helm
```

## Helms install 
[helm install option](https://helm.sh/docs/helm/helm_install/)

-n, --namespace string                namespace scope for this request




## helml pull 

```bash
# 특정 repo 버젼 정보 조회 
helm search repo stable


# download helm chart
helm pull kafka-ui/kafka-ui --insecure-skip-tls-verify

# cp_sr
helm pull confluentinc/cp-helm-charts --version 0.6.1 --insecure-skip-tls-verify


# 문법 확인
helm lint . # Chart.yaml이 있는 경로만

# template 결과물 확인
helm template . 

# 파일을 이용하여 helm install
helm install kafka-ui-init . --dry-run

#### install 
helm install kafka-ui-init . \
--namespace kafka-group \
--set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
--dry-run

# upgrade

helm upgrade kafka-ui-init . \
--set envs.config.KAFKA_CLUSTERS_0_NAME=aicel-kafka-dev \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-3.aicelkafkadev.ht33o6.c2.kafka.ap-northeast-2.amazonaws.com:9092 


# note 확인 
echo http://$NODE_IP:$NODE_PORT
```

## chart structure
- [getting start helm](https://helm.sh/docs/chart_template_guide/getting_started/)
```bash
mychart/
  Chart.yaml
  values.yaml
  charts/
  templates/
  ...
```



# create chart

```bash
helm create mychart

```



## shubchart
- [Subcharts and Global Values](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/)
```
```



- - -

# helm basic 

## 1. helm install repo check
```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh

# 설치 후 버젼 확인
helm version

# stable chart repo 추가
helm repo add stable https://kubernetes-charts.storage.googleapis.com/

# add repo 
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/

# update repo
helm repo update 

# helm install  list
helm repo list 
# 특정 repo 버젼 정보 조회 
helm search repo stable



```

## 2. 상세 조회

```bash
helm inspect [chart/values/readme] <chart name>

```





# kubectl config 
```bash

# 현재 context 확인
kubectl config get-contexts

# context 추가 
kubectl config set-cluster arn:aws:eks:ap-northeast-2:445772965351:cluster/aicel-elt-pipeline-prd

# conext 변경
kubectl config use-context dev-cluster-v1
kubectl config use-context aicel-elt-pipeline-dev
kubectl config use-context aicel-elt-pipeline-prd

# namespace prefix 지정 
kubectl config set-context --current --namespace=kafka-group

# Validate it
kubectl config view --minify | grep namespace:

# 노드 정보 
kubectl get node


# get node yaml 파일 
kubectl get pods/aicel-schema-registry-c5768479-gflxt -o yaml

#
kubectl get deployment.apps/aicel-schema-registry -o yaml
```


# pods 관리
```bash
# shell 접근 ( bin/bash or sh)
kubectl exec --stdin --tty pod/kafka-ui-init-864dbcc7d8-w6wxg -- bin/bash

# pods 의 환경 변수 확인 
kubectl -n kafka-group exec pod/aicel-cp-schema-registry-86c9f46488-w85wn printenv

kubectl -n kafka-group exec pod/kafka-ui-init-5849b668cf-d68dq printenv
```

# yaml 정의 및 삭제 

```bash
# apply
kubectl apply -f 
# delete pods
kubectl delete -f deployment.yaml
kubectl delete deployment my-deployment

# service account 삭제
kubectl delete serviceaccount -n kafka-group sa-kafka-ui

```

# kubectl 설치 
```sh

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

# 구글 공개 샤이니키 다운로드
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

# key 확인 
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list


curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
# 버젼 확인 필요 eks 상에서 12.3.6 버젼이 정상적으로 configmap을 읽어 오지 못하는 이슈 발생 
curl -LO https://dl.k8s.io/release/v1.23.6/bin/linux/amd64/kubectl

# 설치
sudo install -o ubuntu -g ubuntu -m 0755 kubectl /usr/local/bin/kubectl

# 버젼 체크
kubectl version --client --output=yaml    

# aws cluster 추가
# 기존에 만들어진 .kube/config 파일이 있으면 해당 내용 모두 삭제
aws eks update-kubeconfig --region ap-northeast-2 --name aicel-elt-pipeline-prd
# 등록 확인
kubectl config get-contexts

```
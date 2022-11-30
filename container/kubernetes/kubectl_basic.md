


# kubectl config 
```bash

# 현재 context 확인
kubectl config get-contexts

# context 추가 
kubectl config set-cluster arn:aws:eks:ap-northeast-2:445772965351:cluster/aicel-elt-pipeline-prd

# conext 변경
kubectl config use-context dev-cluster-v1
kubectl config use-context aicel-elt-pipeline-dev

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





# yaml 정의 및 삭제 

```bash
# apply
kubectl apply -f 
# delete pods
kubectl delete -f deployment.yaml
kubectl delete deployment my-deployment

```

# kubectl 설치 
```sh

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

# 구글 공개 샤이니키 다운로드
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

#
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list


curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
# 버젼 확인 필요 eks 상에서 12.3.6 버젼이 정상적으로 configmap을 읽어 오지 못하는 이슈 발생 
curl -LO https://dl.k8s.io/release/v1.23.6/bin/linux/amd64/kubectl

# 설치
sudo install -o ubuntu -g ubuntu -m 0755 kubectl /usr/local/bin/kubectl

# 버젼 체크
kubectl version --client --output=yaml    

```
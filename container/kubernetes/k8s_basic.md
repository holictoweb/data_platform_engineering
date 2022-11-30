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


# kubectl eks 사용 
```bash
# 현재 사용중인 권한 확인
aws sts get-caller-identity


# .kube/config 파일 업데이트 
aws eks update-kubeconfig --region ap-northeast-2 --name aicel-elt-pipeline-dev

# 연결된 클러스터 확인
kubectl config get-clusters
```


# oidc 확인
```bash
aws eks describe-cluster --name osf-eks-cluster --query "cluster.identity.oidc.issuer" --output text
```
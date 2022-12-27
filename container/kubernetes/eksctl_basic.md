# eksctl 설치
```bash
# 최신버젼 다운로드 & 압축해제 & /tmp 저장
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

# bin 이동
sudo mv /tmp/eksctl /usr/local/bin



```


# oidc provider 생성
```bash
# oidc enable
eksctl utils associate-iam-oidc-provider --cluster=aicel-elt-pipeline-dev --region=ap-northeast-2  --approve


eksctl utils associate-iam-oidc-provider --cluster=aicel-elt-pipeline-prd --region=ap-northeast-2  --approve



```

# kubernetes config 설정
```bash
# aws eks config 회신화 
# .kube/config 파일이 다른부분은 삭제 하고 진행 필요 
aws eks update-kubeconfig --region ap-northeast-2 --name aicel-elt-pipeline-dev

# 1. eks 에 aws 사용자 추가 
# kubectl 사용등 kubernetes 에 대한 권한 필요 
aws eks update-kubeconfig --name aicel-elt-pipeline-dev --region ap-northeast-2 --role-arn arn:aws:iam::445772965351:user/holictoweb


aws eks update-kubeconfig --name aicel-elt-pipeline-dev --region ap-northeast-2 --role-arn arn:aws:iam::445772965351:role/aicel-prod-workflow-role

# 2. 계정 연결 정보 확인 ( 개인 계정으로 eks 접근 권한 확인 )
eksctl get iamidentitymapping --cluster aicel-elt-pipeline-dev --region=ap-northeast-2
```

# service account & iam 연결 생성 
```bash
#  iam service account 생성
eksctl create iamserviceaccount --name sa-schema-registry \
--namespace kafka-group \
--cluster aicel-elt-pipeline-dev \
--attach-policy-arn arn:aws:iam::445772965351:policy/AmazonMSK-aicel-kafka-prd-rw \
--approve \
--override-existing-serviceaccounts \
--role-name eksctl-serviceaccount-schema-registry-prd

# service account 조회
eksctl get iamserviceaccount --cluster dev-cluster-v1
eksctl get iamserviceaccount --cluster aicel-elt-pipeline-dev

# (ToDo) delete service account

# iamsericeaccount 연결
eksctl get iamserviceaccount --cluster aicel-elt-pipeline-dev --region=ap-northeast-2


# node 정보
eksctl get nodegroup --cluster=aicel-elt-pipeline-dev
```


# config 파일 예시 
```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: 
    server: https://46F83EEC1E1D326D0A95A0E9AADE534B.gr7.ap-northeast-2.eks.amazonaws.com
  name: arn:aws:eks:ap-northeast-2:445772965351:cluster/aicel-elt-pipeline-prd
contexts:
- context:
    cluster: arn:aws:eks:ap-northeast-2:445772965351:cluster/aicel-elt-pipeline-prd
    namespace: kafka-group
    user: arn:aws:eks:ap-northeast-2:445772965351:cluster/aicel-elt-pipeline-prd
  name: aicel-elt-pipeline-prd
current-context: aicel-elt-pipeline-prd
kind: Config
preferences: {}
users:
- name: arn:aws:eks:ap-northeast-2:445772965351:cluster/aicel-elt-pipeline-prd
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      args:
      - --region
      - ap-northeast-2
      - eks
      - get-token
      - --cluster-name
      - aicel-elt-pipeline-prd
      command: aws
      env: null
      interactiveMode: IfAvailable
      provideClusterInfo: false



```
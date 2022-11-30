
# oidc provider 생성
```bash
# oidc enable
eksctl utils associate-iam-oidc-provider --cluster=aicel-elt-pipeline-dev --approve

```

# kubernetes config 설정
```bash
# aws eks config map 회신화 
aws eks update-kubeconfig --region ap-northeast-2 --name aicel-elt-pipeline-dev

# 사용자 추가 
aws eks update-kubeconfig --name aicel-elt-pipeline-dev --region ap-northeast-2 --role-arn arn:aws:iam::445772965351:user/holictoweb

# service account 조회
eksctl get iamserviceaccount --cluster dev-cluster-v1
eksctl get iamserviceaccount --cluster aicel-elt-pipeline-dev

# 계정 연결 정보 확인 ( 개인 계정으로 eks 접근 권한 확인 )
eksctl get iamidentitymapping --cluster aicel-elt-pipeline-dev --region=ap-northeast-2

# node 정보
eksctl get nodegroup --cluster=aicel-elt-pipeline-dev
```






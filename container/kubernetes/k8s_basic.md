


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
aws eks describe-cluster --name dev-cluser-v1 --query "cluster.identity.oidc.issuer" --output text
```
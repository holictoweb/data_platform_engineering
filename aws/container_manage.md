### private vpc 에서 구성 된 ec2 에서 ecr에 접근 

1. ecr dkr endpoint 생성
   
2. endpoint의 securty group 에서 443으로 인바운드 오픈


3. ecr 사용을 위한 credentials 설정 

- ecr repository 생성 
```bash
aws ecr create-repository \
     --repository-name lji-repo-name \
     --region us-west-2
```
- 해당 repo의 로그인 정보 저장
```bash
aws ecr get-login-password \
      --region us-west-2 | docker login \
      --username AWS \
      --password-stdin 378010018656.dkr.ecr.us-west-2.amazonaws.com

=========================================================================================
WARNING! Your password will be stored unencrypted in /home/ubuntu/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

```




# aws 공식 이미지를 사용 하기 위해서 해당 ecr로 로그인이 필요 
```
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.ap-northeast-2.amazonaws.com


```

```
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/ml/serve-fasttext

```


# 이미지 지정 방법 

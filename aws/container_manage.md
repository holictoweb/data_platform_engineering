### private vpc 에서 구성 된 ec2 에서 ecr에 접근 

1. ecr dkr endpoint 생성
   
2. endpoint의 securty group 에서 443으로 인바운드 오픈


3. ecr 사용을 위한 credentials 설정 

- ecr repository 생성 
```
aws ecr create-repository \
     --repository-name lji-repo-name \
     --region us-west-2
```
- 해당 repo의 로그인 정보 저장
```
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

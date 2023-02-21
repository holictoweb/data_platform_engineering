

## 기본 이미지 다운로드


```bash
sudo docker pull python:3.8.10-slim-buster

fullname="3109239284284.dkr.ecr.us-west-2.amazonaws.com/python:3.8.10-slim-buster"
# docker images 를 통해 해당 image id 를 확인 해당 image 에 tag 정보 등록 
docker tag f2c36f6f6523 ${fullname}

# repository 가 지정 됨
REPOSITORY                                            TAG                  IMAGE ID            CREATED             SIZE
3109239284284.dkr.ecr.us-west-2.amazonaws.com/python   3.8.10-slim-buster   f2c36f6f6523        2 weeks ago         114MB
python                                                3.8.10-slim-buster   f2c36f6f6523        2 weeks ago         114MB




```


## aws ecr login and push 
```bash
# ecr login 
aws ecr get-login-password --region us-west-2|docker login --username AWS --password-stdin ${fullname}

docker push ${fullname}

aws ecr get-login-password --region ap-northeast-2|docker login --username AWS --password-stdin 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/aicel-news-cluster-lib-prod

aws ecr get-login-password --region ap-northeast-2|docker login --username AWS --password-stdin 23232.dkr.ecr.ap-northeast-2.amazonaws.com/aicel-news-cluster-lib-prod


aws ecr get-login-password --region ap-northeast-2|docker login --username AWS --password-stdin 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/

```




```bash 
# simple login 
aws ecr get-login-password --region ap-northeast-2| docker login --username AWS --password-stdin 3232.dkr.ecr.ap-northeast-2.amazonaws.com


```

# build and push

```bash
#!/bin/bash
full_name='445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/dev-aicel'
tag='dev-lji-crawler'
region='ap-northeast-2'
aws ecr get-login-password --region ap-northeast-2|docker login --username AWS --password-stdin 23929394.dkr.ecr.ap-northeast-2.amazonaws.com/dev-aicel

# build with tag
docker build -t $tag .

docker tag $tag ${full_name}:${tag}
docker push ${full_name}:${tag}


```


```bash
docker build -t dev-schema-registry
docker tag dev-schema-registry 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/aicel-schema-registry:dev-schema-registry

docker push 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/aicel-schema-registry:dev-schema-registry
```




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
```
# ecr login 
aws ecr get-login-password --region us-west-2|docker login --username AWS --password-stdin ${fullname}


docker push ${fullname}



aws ecr get-login-password --region ap-northeast-2|docker login --username AWS --password-stdin 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com/dev-aicel



```




```bash 
# simple login 
aws ecr get-login-password --region ap-northeast-2| docker login --username AWS --password-stdin 445772965351.dkr.ecr.ap-northeast-2.amazonaws.com



```
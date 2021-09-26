
- 모든 docker ps 삭제
- 모든 docker images 삭제 
```shell
# container 전체 삭제 
docker ps -aq
docker rm $(docker ps -aq)

# 이미지 전체 삭제 
docker images 
docker rmi $(docker images -q)

```

- image 삭제 중 오류 메세지
- ecr에 레파지토리가 변경되면서 여러곳에 등록이 되어 발생하는 문제로 보임.
```
Error response from daemon: conflict: unable to delete 4d78bd50b6a3 (must be forced) - image is referenced in multiple repositories

# 위와 같은 에러 발생 시 일단 -f 옵션 처리
docker rmi -f 4d78bd50b6a3
```

- child image 에러
```
Error response from daemon: conflict: unable to delete f7de38042ce0 (cannot be forced) - image has dependent child images

```


- docker build

```
docker build -t {tag명} ./Dockerfile 경로


```



# Docker image 관련

- docker image의 세부 정보 확인 가능. 
```
docker image inspect f7de38042ce0
```



# docker 설치 


```sh
# 업데이트 진행 
apt update & apt upgrade


# 필수 패키지 설치 
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# GPG Key 인증
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# arch 확인
arch

# repo 등록

sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"

# Docker 설치를 위하 준비가 끝. 설치 진행
sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io

```

# docker 실행

- 데몬 수행

``` sh
# 권한 부여 기본적으로  root 권한이 필요 
sudo usermod -aG docker $USER # 현재 접속중인 사용자에게 권한주기
sudo usermod -aG docker your-user # your-user 사용자에게 권한주기

# docker 등록 및 수행 
sudo systemctl enable docker 
sudo service docker start


sudo service docker stop
sudo service docker restart

# 위에 service로 실행 하는것과 아래 방식의 차이 확인 필요 
sudo /etc/init.d/docker start 
```











# docker file basic


```python
FROM openjdk:8-jdk-alpine

RUN apk --no-cache add tzdata && cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime

WORKDIR /app
COPY hello.jar hello.jar
COPY test.py
RUN chmod 774 test.py

ENTRYPOINT ["python test.py"]
```


FROM : 이미지를 생성할 때 사용할 기반 이미지를 지정한다. 
RUN : 이미지를 생성할 때 실행할 코드를 지정한다. 예제에서는 패키지를 설치하고 파일 권한을 변경하기 위해 RUN을 사용했다.
WORKDIR : 작업 디렉토리를 지정한다. 해당 디렉토리가 없으면 새로 생성한다.   
    작업 디렉토리를 지정하면 그 이후 명령어는 해당 디렉토리를 기준으로 동작한다.  
COPY : 파일이나 폴더를 이미지에 복사한다. 위 코드에서 두 번째 COPY 메서드는 entrypoint.sh 파일을 이미지에 run.sh 이름으로 복사한다. 상대 경로를 사용할 경우 WORKDIR로 지정한 디렉토리를 기준으로 복사한다.
ENV : 이미지에서 사용할 환경 변수 값을 지정한다. 위 코드는 PROFILE 환경 변수의 값으로 local을 지정했는데 이 경우 컨테이너를 생성할 때 PROFILE 환경 변수를 따로 지정하지 않으면 local을 기본 값으로 사용한다.
ENTRYPOINT : 컨테이너를 구동할 때 실행할 명령어를 지정한다. 위에서는 run.sh을 실행하도록 설정했다.



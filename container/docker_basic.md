
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

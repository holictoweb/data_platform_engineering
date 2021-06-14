
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

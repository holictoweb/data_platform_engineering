
- 모든 docker ps 삭제

```shell
docker ps -aq
docker rm $(docker ps -aq)

```

- docker build

```
docker build -t {tag명} ./Dockerfile 경로


```

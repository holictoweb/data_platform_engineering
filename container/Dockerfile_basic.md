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



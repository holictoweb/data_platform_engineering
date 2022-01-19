
```py
client = boto3.client('ecs')
```


# task 리스트 조회 


```py
response = client.list_tasks(
    cluster='string',
    containerInstance='string',
    family='string',
    nextToken='string',
    maxResults=123,
    startedBy='string',
    serviceName='string',
    desiredStatus='RUNNING'|'PENDING'|'STOPPED',
    launchType='EC2'|'FARGATE'|'EXTERNAL'
)


# 기본 조회
res = client.list_tasks( cluster='tf-dev-cluster-vst', desiredStatus='RUNNING', launchType='FARGATE' )


```


# task 상세 정보 조회
```py
response = client.describe_tasks(
    cluster='string',
    tasks=[
        'string',
    ],
    include=[
        'TAGS',
    ]
)


response = client.describe_tasks(cluster='tf-dev-cluster-vst', task='arn:aws:ecs:ap-northeast-2:445772965351:task/tf-dev-cluster-vst/0c72b37602fd430a9dc17ea60dff19f7')


```

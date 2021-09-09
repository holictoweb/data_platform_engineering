[ecs connect exec ](#ecs_fargate_connect)
[ecs cluster 생성 하기](#ecs_cluster)

# ref
1. [NEW – Using Amazon ECS Exec to access your containers on AWS Fargate and Amazon EC2](!https://aws.amazon.com/ko/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/)
2. [디버깅을 위해 Amazon ECS Exec 사용](!https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs-exec.html)


 - - - 


### ecs 정보 조회 

```bash

# cluster list 조회 
aws ecs list-clusters

# cluster 상의 task 조회
aws ecs list-tasks  --cluster tf-dev-cluster-vst
```


# ecs fargate connect
https://aws.amazon.com/ko/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/


> **Server-side requirements (AWS Fargate)**  
> If the ECS task and its container(s) are running on Fargate, there is nothing you need to do because Fargate already includes all the infrastructure software requirements to enable this ECS capability. Because the Fargate software stack is managed through so called “Platform Versions” (read this blog if you want have an AWS Fargate Platform Versions primer), you only need to make sure that you are using PV 1.4 (which is the most recent version and ships with the ECS Exec prerequisites).


> **Client-side requirements**  
> If you are using the AWS CLI to initiate the exec command, the only package you need to install is the SSM Session Manager plugin for the AWS CLI. Depending on the platform you are using (Linux, Mac, Windows) you need to set up the proper binaries per the instructions. Today, the AWS CLI v1 has been updated to include this logic. The AWS CLI v2 will be updated in the coming weeks. Remember also to upgrade the AWS CLI v1 to the latest version available. This version includes the additional ECS Exec logic and the ability to hook the Session Manager plugin to initiate the secure connection into the container.




### ecs 에서 수행 중인 task 에 대한 정보 확인 
```bash
AWS_REGION="ap-northeast-2"

aws ecs describe-tasks \
    --cluster tf-dev-cluster-vst \
    --region $AWS_REGION \
    --tasks eeb0a1e3dc3240b5ac2c538c88b3873b

aws ecs describe-tasks \
    --cluster tf-dev-cluster-vst \
    --tasks 6c94908f34724ae3b5361139af0ca0ee
```

### ecs job(task) definition 조회
```bash
aws ecs describe-task-definition --task-definition ncc_job_creator
```


### session manager install
- ecs execute-command를 사용하기 위해서는 SSM session manager 를 설치 해야함. 
https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

```bash
# aws linux
# download x86-64
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/linux_64bit/session-manager-plugin.rpm" -o "session-manager-plugin.rpm"

# install
sudo yum install -y session-manager-plugin.rpm
```

```bash
# ubuntu
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"

#install
sudo dpkg -i session-manager-plugin.deb
```


### ecs fargate container 접속 

```bash
aws ecs execute-command  \
    --region $AWS_REGION \
    --cluster tf-dev-cluster-vst \
    --task 7225d5c329bf46198a61c50a938f383a \
    --container ncc_crawler \
    --command "/bin/bash" \
    --interactive


aws ecs execute-command 
    --cluster cluster-name \
    --task task-id \
    --container container-name \
    --interactive \
    --command "/bin/sh"

```


#### error 
```bash
holictoweb@LAPTOP-NGM0A0IK:~/download$ aws ecs execute-command  \
>     --region $AWS_REGION \
>     --cluster tf-dev-cluster-vst \
>     --task 6c94908f34724ae3b5361139af0ca0ee \
>     --container ncc_crawler \
>     --command "/bin/bash" \
>     --interactive

The Session Manager plugin was installed successfully. Use the AWS CLI to start a session.


An error occurred (InvalidParameterException) when calling the ExecuteCommand operation: The execute command failed because execute command was not enabled when the task was run or the execute command agent isn’t running. Wait and try again or run a new task with execute command enabled and try again.

# client 상에는 최신 aws cli와 session manager 설치
# server ( fargate ) 상에는 실행 시   enableExecuteCommand가 true 로 설정 되어야함. 
"cpu": "1024",
"createdAt": "2021-09-06T01:00:07.344000+09:00",
"desiredStatus": "RUNNING",
"enableExecuteCommand": false,
"group": "family:ncc_crawler",
"healthStatus": "UNKNOWN",
```


#### 개별 container 실행 방법
```bash
aws ecs create-service \
    --cluster tf-dev-cluster-vst \
    --task-definition ncc_crawler \
    --enable-execute-command \
    --service-name cli-create \
    --desired-count 1



```



# dev ecs fartgate connect 
```
aws ecs execute-command 
    --cluster cluster-name \
    --task task-id \
    --container container-name \
    --interactive \
    --command "/bin/sh"

```




# ecs cluster
## ecs cluster 조회 및 동일한 형태의 cluster 생성
1. cluster list 조회 

```bash
# cluster list
aws ecs list-clusters

# cluster detail 
aws ecs describe-clusters --cluster dev-aicel-cluster

```


2. task definition 확인
```
# task definition 조회  리스트 
aws ecs list-task-definitions --family-prefix dev-task-definition-01

# task definition 상세 
aws ecs describe-task-definition --task-definition dev-task-definition-01:2


# 현재 수행 중인 task 
aws ecs list-tasks  --cluster dev-aicel-cluster
aws ecs describe-tasks \
    --cluster dev-aicel-cluster \
    --tasks bc714392c07643f5914de71e0d3e95aa


aws ecs describe-tasks \
    --cluster tf-dev-cluster-vst \
    --tasks 0ce67e8882a848558357c3eaf72752dc
```

3. task 실행 시 exec 
```bash


# 아래는 service 생성으로 task 생성과는 다른 작업 
aws ecs create-service \
    --cluster dev-aicel-cluster \
    --task-definition dev-task-definition-01 \
    --enable-execute-command \
    --service-name dev-test-01 \
    --network-configuration "awsvpcConfiguration={subnets=[ subnet-a56f08cc]}" \
    --desired-count 1

```
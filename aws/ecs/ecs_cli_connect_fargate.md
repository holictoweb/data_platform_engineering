[ecs connect exec ](#ecs_fargate_connect)
[ecs cluster 생성 하기](#ecs_cluster)

# ref
1. [NEW – Using Amazon ECS Exec to access your containers on AWS Fargate and Amazon EC2](!https://aws.amazon.com/ko/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/)
2. [디버깅을 위해 Amazon ECS Exec 사용](!https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs-exec.html)


- - -


# ecs fargate connect
https://aws.amazon.com/ko/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/


> **Server-side requirements (AWS Fargate)**  
> If the ECS task and its container(s) are running on Fargate, there is nothing you need to do because Fargate already includes all the infrastructure software requirements to enable this ECS capability. Because the Fargate software stack is managed through so called “Platform Versions” (read this blog if you want have an AWS Fargate Platform Versions primer), you only need to make sure that you are using PV 1.4 (which is the most recent version and ships with the ECS Exec prerequisites).


> **Client-side requirements**  
> If you are using the AWS CLI to initiate the exec command, the only package you need to install is the SSM Session Manager plugin for the AWS CLI. Depending on the platform you are using (Linux, Mac, Windows) you need to set up the proper binaries per the instructions. Today, the AWS CLI v1 has been updated to include this logic. The AWS CLI v2 will be updated in the coming weeks. Remember also to upgrade the AWS CLI v1 to the latest version available. This version includes the additional ECS Exec logic and the ability to hook the Session Manager plugin to initiate the secure connection into the container.



# 1. root filesystem 사용 활성화 
```bash
An error occurred (TargetNotConnectedException) when calling the ExecuteCommand operation: The execute command failed due to an internal error. Try again later.

# 위와 같은 오류가 발생 하는 것은 ssm 이 실제 root filesystem 상에 쓰기 기능이 있어야만 정상 동작 하기 때문임
readonlyRootFilesystem = false
```

# 2. ssm 상에  channel을 열수 있는 권한 필요 
- task execution role 상에 추가   
ssmmessages:CreateControlChannel  
ssmmessages:createDatchannel  
ssmmessages:OpenControlChannel  
ssmmessages:OpenDataChannel  
```bash
# task execution role 상에 아래 policy 추가 
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        }
    ]
}
```

# 3. session manager install
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


# 4.  enable exec command 활성화

## 1. task job schedueler에서 활성화 
https://docs.aws.amazon.com/AmazonECS/latest/userguide/scheduled_tasks.html  
>(Optional) Expand Configure additional properties to specify the following additional parameters for your tasks.
>For Task group, specify a task group name. The task group name is used to identify a set of related tasks and is used in conjunction with the spread task placement strategy to ensure tasks in the same task group are spread out evently among the container instances in the cluster.  
>For Tags, choose Add tag to associate key value pair tags for the task.  
>For Configure managed tags, choose Enable managed tags to have Amazon ECS add tags that can be used when reviewing cost allocation in your Cost and Usage Report. For more information, see Tagging your resources for billing.  
>For Configure execute command, choose Enable execute command to enable the ECS Exec functionality for the task. For more information, see Using Amazon ECS Exec for debugging.  
>For Configure propagate tags, choose Propagate tags from task definition to have Amazon ECS add the tags associated with the task definition to your task. For more information, see Tagging your resources.  



### 2. 개별 container 실행 및 접속 
```bash

aws ecs run-task \
    --cluster dev-aicel-cluster  \
    --task-definition dev-task-definition-02 \
    --network-configuration awsvpcConfiguration="{subnets=['subnet-246db769'],assignPublicIp=ENABLED}" \
    --enable-execute-command \
    --launch-type FARGATE \
    --tags key=environment,value=production \
    --platform-version '1.4.0' \
    --region ap-northeast-2


# 생성 후 task 확인 
aws ecs describe-tasks \
    --cluster dev-aicel-cluster \	
    --tasks 88cde14d6c4d4e30a3d75403f7d22d7d

```



# 5. ecs exec 접속

### ecs fargate container 접속 방법
```bash
AWS_REGION="ap-northeast-2"

aws ecs execute-command  \
    --region $AWS_REGION \
    --cluster tf-dev-cluster-vst \
    --task de79e8ca8ff442478fe0f79e043c68a1 \
    --container ncc_crawler \
    --command "/bin/bash" \
    --interactive

aws ecs execute-command \
    --region $AWS_REGION \
    --cluster dev-aicel-cluster \
    --task 488cf17c303b4d569b3db4ced408617b \
    --container dev-task-definition-02 \
    --interactive \
    --command "/bin/sh"

aws ecs execute-command \
    --region ap-northeast-2 \
    --cluster dev-aicel-cluster \
    --task 33f9704effdb49f69ac62ca007907a59 \
    --container dev-task-definition-02 \
    --interactive \
    --command "/bin/bash"

aws ecs execute-command \
    --region ap-northeast-2 \
    --cluster dev-aicel-cluster \
    --task ad726d4b05fc4845a163ac15d687153c \
    --container dev-task-definition-02 \
    --interactive \
    --command "ls"

```

   



# 기본 조회 기능 

### ecs 정보 조회 

```bash

# cluster list 조회 
aws ecs list-clusters

# cluster 상의 task 조회
aws ecs list-tasks  --cluster tf-dev-cluster-vst
```

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



# error 
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



## ecs cluster 조회 및 동일한 형태의 cluster 생성
1. cluster list 조회 

```bash
# cluster list
aws ecs list-clusters

# cluster detail 
aws ecs describe-clusters --cluster dev-aicel-cluster

```


2. task definition 확인
```bash
# task definition 조회  리스트 
aws ecs list-task-definitions --family-prefix dev-task-definition-01

# task definition 상세 
aws ecs describe-task-definition --task-definition dev-task-definition-02


# 현재 수행 중인 task 
aws ecs list-tasks  --cluster dev-aicel-cluster
aws ecs describe-tasks \
    --cluster dev-aicel-cluster \
    --tasks ad726d4b05fc4845a163ac15d687153c


aws ecs describe-tasks \
    --cluster tf-dev-cluster-vst \
    --tasks 0ce67e8882a848558357c3eaf72752dc
```

# ECS CHECK 

[Amazon ECS Exec Checker](!https://github.com/aws-containers/amazon-ecs-exec-checker)
- shell을 통해 현재 구성에 이슈가 없는지 확인 가능. 
```bash
# param : cluster name / task id
./check-ecs-exec.sh dev-aicel-cluster b27d15e151bf443088453a0e7f8b96f2
```








# 스토리지 추가

- 볼륨 크기 조정 후 Linux 파일 시스템 확장

- https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html
- 

``` bash
# lsblk를 사용하여 시작 시에 매핑되지 않았지만 포맷되고 마운트된 볼륨을 봅니다.
lsblk

nvme0n1     259:0    0  100G  0 disk 
└─nvme0n1p1 259:1    0   20G  0 part /

# 

# 용량 확인 
df -hT

# 현재 스트리지 구성 확인 
lsblk 


# 용량을 늘려야 할 대상 part 선택 
sudo growpart /dev/nvme0n1 1
```



# elb 추가

```
```


# boto3

```py
# Boto 3
import boto3
ec2 = boto3.resource('ec2')

# check running instance
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type)


```

## ebs volume list

```py


```

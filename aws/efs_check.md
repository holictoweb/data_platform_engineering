# EFS 생성 
```bash

# unmount 
umount /mnt/efs

# mount 대상 생성
mkdir ~/airflow/dags


# util 설치 
sudo apt install awscli
sudo apt-get install nfs-common 

# mount efs (efs 콘솔의 attch 버튼을 통해 확인 가능 )
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-0335cd93fd5b85996.efs.ap-northeast-2.amazonaws.com:/ ~/airflow/dags

# mount 후에 루트 사용자에 권한 추가
cd ~/airflow/dags
sudo chmod go+rw .
```



## EFS mount 확인


- 마운트 정보 확인 
```bash
# tree 
findmnt

# fstab output list
# /etc/fstab file and /etc/fstab.d
findmnt -s

output 
TARGET           SOURCE                                    FSTYPE OPTIONS
/                UUID=b24eb1ea-ab1c-47bd-8542-3fd6059814ae xfs    defaults,noatime
/mnt/efs/airflow fs-14617375:/                             efs    _netdev,tls,iam
```

- findmnt -s 를 통해 efs-id 확인 가능 


### efs가 마운트 되어 있는 대상 확인




### efs 마운트
https://docs.aws.amazon.com/ko_kr/efs/latest/ug/wt1-test.html

efs console 에서는 dns 를 확인 할 수 없음
> file-system-id.efs.aws-region.amazonaws.com 
> fs-1757e577.efs.ap-northeast-2.amazonaws.com

- efs -> network 
  - security group 확인 ( 마운트 시킬 대상 ec2 sg를 포함하는것도 방법 ) 
  - mount name 확인 

```
mkdir ~/efs-mount-point 

sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport mount-target-DNS:/   ~/efs-mount-point  

```

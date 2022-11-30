

# EBS 암호화

## 레퍼런스
- prod dev (https://aws.amazon.com/ko/blogs/korea/new-opt-in-to-default-encryption-for-new-ebs-volumes/)
- 기본 encrypt 사항 ()

- You cannot directly encrypt existing unencrypted volumes or snapshots. 
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-parameters

- ec2 빠른 복원 문제 해결을 위한 루트 볼륨 대체 
- https://aws.amazon.com/ko/about-aws/whats-new/2021/04/ec2-enables-replacing-root-volumes-for-quick-restoration-and-troubleshooting/

- EKS PV encrpt
- https://skildops.com/blog/encrypt-an-existing-k8s-pv-running-on-aws-eks

- crete AMI with encrypted EBS snapshots 
- https://aws.amazon.com/ko/blogs/security/how-to-create-a-custom-ami-with-encrypted-amazon-ebs-snapshots-and-share-it-with-other-accounts-and-regions/


## limitation 
- ebs 지원 가능 여부 
https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/EBSEncryption.html#EBSEncryption_supported_instances


## prerequists
- volume 자체에 대한 변경은 불가
- snapshot 을 통해 변경된 ( encrypt 추가 혹은 변경) volume 을 스냅샷을 통해 생성 후 교체 하는 방식.

## device 정보 
- https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/device_naming.html




## senario
### create KMS key ( data key - symmentric key )


## 1. activate encrypt
- 기본 암호화 활성화 ( 이후 생성되는 volume에 대한 디폴트 설정 )
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#encryption-by-default
```
To configure the default KMS key for EBS encryption for a Region
1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.
2. From the navigation bar, select the Region.
3. From the navigation pane, select EC2 Dashboard.
4. In the upper-right corner of the page, choose Account Attributes, EBS encryption.
5. Choose Manage.
6. For Default encryption key, choose a symmetric customer managed encryption key.
7. Choose Update EBS encryption.
```

## 2. 암호화 되지 않은 볼륨 복원
![](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/images/volume-encrypt-account-off.png)

![](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/images/volume-encrypt-account-on.png)

### snapshot volume with kms
https://docs.aws.amazon.com/cli/latest/reference/ec2/create-snapshot.html


### aws senario
https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/EBSEncryption.html#snapshot-account-off



# boto3 ebs

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html
can_paginate()
close()
complete_snapshot()
get_paginator()
get_snapshot_block()
get_waiter()
list_changed_blocks()
list_snapshot_blocks()
put_snapshot_block()
start_snapshot()

- aicel-work-flow i-0864346043342d3f0 vol-04a59d5430744052a

## 1. CMK 생성
- key polices in aws kms
- https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-users
- 사용자 / policy 등은 추후에 추가 샂게 가능 하므로 일단 삭제 가능한 계정만 지정 

## 2. snapshot 생성 

```py
import boto3
AWS_REGION = "ap-northeast-2"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
VOLUME_ID = 'vol-04a59d5430744052a'
snapshot = EC2_RESOURCE.create_snapshot(
VolumeId=VOLUME_ID,
TagSpecifications=[
    {
        'ResourceType': 'snapshot',
        'Tags': [
            {
            'Key': 'Name',
            'Value': 'aicel-work-flow-ebs-snapshot'
            },
        ]
    },
]
```
## 3. snapshot 으로 암호화된 snapshot 생성
```py
# snapshot 복사본 생성 with encrypt

# snapshot 생성 
import boto3
AWS_REGION = "ap-northeast-2"
ec2_client = boto3.client('ec2', region_name=AWS_REGION)

snapshot_id  = 'snap-0b6e85a43f570b465'
kms_key_id='2e7feb88-9248-410d-bb6a-fc031f422320'
# instance_id = 

DryRunFlag = False


    
try:
    response = ec2_client.copy_snapshot(
            SourceRegion=AWS_REGION,
            SourceSnapshotId=snapshot_id,
            Encrypted=True,
            KmsKeyId=kms_key_id,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                        'Key': 'Name',
                        'Value': instance_name + '-ebs-snapshot-copy-encrypt'
                        },
                    ],
                },
            ],
            Description='Snapshot of copy ({})'.format(snapshot_id)
        )
    if response['ResponseMetadata']['HTTPStatusCode']== 200:
        encrypt_snapshot_id= response['SnapshotId']
        print('***encrypt_snapshot_id:', encrypt_snapshot_id)
    
        ec2_client.get_waiter('snapshot_completed').wait(
            SnapshotIds=[encrypt_snapshot_id],
            DryRun=DryRunFlag
            )
        print('***Success!! encrypt_snapshot_id :', encrypt_snapshot_id, 'created...')
        
except Exception as e:
        print('***Failed to copy the snapshot ...')
        print(type(e), ':', e)

```


## 4. ~~암호화된 snapshot을 통해 root volume replace task 생성~~
```bash
aws ec2 create-replace-root-volume-task --instance-id i-0864346043342d3f0 --snapshot-id snap-028ba6522762484f6
# default ebs 암호화 설정 시 암호화 되지 않은 snapshot으로 root volume replace 할 경우 처리 확인 필요 

# 실제 volume id가 할당 되지 않은 snapshot은 타스크 생성 불가
An error occurred (InvalidParameterValue) when calling the CreateReplaceRootVolumeTask operation: Invalid snapshot for root volume for virt i-0864346043342d3f0. The snapshot should be of one of the root volumes attached to the instance in the past

```

## 3. snapshot 으로 ebs volume 생성
```py
import boto3
from pprint import pprint

AWS_REGION = "ap-northeast-2"

ec2_client = boto3.client('ec2', region_name=AWS_REGION)
try:
    new_volume = ec2_client.create_volume(
        AvailabilityZone=f'{AWS_REGION}a',
        Encrypted=True,
        KmsKeyId='2e7feb88-9248-410d-bb6a-fc031f422320',
        SnapshotId='snap-07d9852389ee93eac',
        Size=100,
        VolumeType='gp2',
        TagSpecifications=[
                {
                    'ResourceType': 'volume',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'aicel-workflow-ebs-snapshot-resotre-2'
                        }
                    ]
                }
            ]
        )
        
    pprint(new_volume["VolumeId"])
    pprint(new_volume)
    
    if response['ResponseMetadata']['HTTPStatusCode']== 200:
            volume_id= response['VolumeId']
            print('***volume:', volume_id)
    
            ec2_client.get_waiter('volume_available').wait(
                VolumeIds=[volume_id],
                DryRun=DryRunFlag
                )
            print('***Success!! volume:', volume_id, 'created...')


except Exception as e:
        print('***Failed to create the volume...')
        print(type(e), ':', e)

```





## 4. attach ebs
```bash
aws ec2 attach-volume --volume-id vol-1234567890abcdef0 --instance-id i-01474ef662b89480 --device /dev/sdf
```

```py
instance_id = 'i-0864346043342d3f0'

DryRunFlag = False
device = '/dev/xvda'


try:
    print('***attaching volume:', volume_id, 'to:', instance_id)
    response= ec2_client.attach_volume(
        Device=device,
        InstanceId=instance_id,
        VolumeId=volume_id,
        DryRun=DryRunFlag
        )
    #pprint(response)

    if response['ResponseMetadata']['HTTPStatusCode']== 200:
        ec2_client.get_waiter('volume_in_use').wait(
            VolumeIds=[volume_id],
            DryRun=False
            )
        print('***Success!! volume:', volume_id, 'is attached to instance:', instance_id)

except Exception as e:
    print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
    print(type(e), ':', e)
```

## detach ebs
```py

# Detaching EBS volume from EC2 instance
import boto3

AWS_REGION = "us-east-2"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
EC2_CLIENT = boto3.client('ec2', region_name=AWS_REGION)

volume = EC2_RESOURCE.Volume('vol-0d4abbb9e7da7ed9f')
instance_id = 'i-0864346043342d3f0'


try:
    print(f'Volume {volume.id} status -> {volume.state}')

    volume.detach_from_instance(
        Device='/dev/sdh',
        InstanceId=instance_id
    )

    # Vaiting for volume to become available
    if response['ResponseMetadata']['HTTPStatusCode']== 200:
        ec2_client.get_waiter('volume_available').wait(
            VolumeIds=[volume_id],
            DryRun=False
            )
        print('***Success!! volume:', volume_id, 'is dettached from instance:', instance_id)


except Exception as e:
    print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
    print(type(e), ':', e)
```

## 5. mount device

```cmd
sudo mount /dev/sdb ~/mnt_snap/
```





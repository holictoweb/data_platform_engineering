import json
import boto3
from datetime import datetime, timedelta

filters = [ 
    {
        'Name': 'instance-state-name', 
        'Values': ['running']
    }
]

region_name = "us-west-2"
ec2 = boto3.client('ec2', region_name=region_name)
cloudwatch = boto3.client('cloudwatch', region_name=region_name)

print(region_name + '의 중지 대상 EC2의 info')
ec2_list = boto3.resource('ec2', region_name = region_name)
# running중인 Instance 추출
instances = ec2_list.instances.filter(Filters=filters)
for instance in instances:
    try:
        tag_list = list()

        # tag의 key 값만 추출
        for i in range(len(instance.tags)):
            tag_list.append(instance.tags[i]['Key'].strip().lower())
        
        # 반복된 key 제거
        tag_list = list(set(tag_list))
        
        if 'aws:elasticmapreduce:job-flow-id' not in tag_list:
            print("현재 tag의 key값 : {}".format(tag_list), instance.id)
            
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instance.id
                    },
                ],
                StartTime=datetime.now() - timedelta(seconds=600),
                EndTime=datetime.now(),
                Period=86400,
                Statistics=[
                    'Maximum',
                ],
                Unit='Percent'
            )
            for cpu in response['Datapoints']:
                if 'Maximum' in cpu:
                    print(instance.id,"의 1시간 최대 CPU 사용률 : ",cpu['Maximum'],"%")

    except Exception as e:
        print(e)

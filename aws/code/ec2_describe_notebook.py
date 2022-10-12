import pandas as pd
from pprint import pprint
import boto3
#Name Tag
def get_tag(each, tag_name):
    if 'Tags' in each:
        for tag in each['Tags']:
          if tag['Key'] == tag_name:
              return tag['Value']
    return ''

#Volumes
def get_vol(each, ec2):
    resultVol = {
        "vol_id": "",
        "vol_size": "",
        "vol_type": ""
    }
    resp = ec2.describe_volumes(
        Filters=[{'Name':'attachment.instance-id','Values':[each['InstanceId']]}]
    )
    for volume in (resp["Volumes"]):
        resultVol['vol_id'] += (str(volume["VolumeId"]) + "\n")
        resultVol['vol_size'] += (str(volume["Size"]) + "\n")
        resultVol['vol_type'] += (str(volume["VolumeType"]) + "\n")

    return resultVol

#Security Groups
def sec_gp(each, ec2):
    resultSG = {
        "sg_id": "",
        "sg_name": ""
    }
    for sg in each['SecurityGroups']:
        resultSG['sg_id'] += (str(sg["GroupId"]) + "\n")
        resultSG['sg_name'] += (str(sg["GroupName"]) + "\n")

    return resultSG

volume_id_list=[]
result = []
    
ec2_client = boto3.client('ec2', region_name="ap-northeast-2")
response = ec2.describe_instances()
# pprint(response)
for item in response["Reservations"]:
    for each in item['Instances']:
        volsss = get_vol(each, ec2)
        sgss = sec_gp(each, ec2)
        #print(sgss)
        result.append({
            'ImageId': each.get('ImageId', ''),
            'InstanceType': each.get('InstanceType', ''),
            'PublicIp': each.get('PublicIpAddress', ''),
            'PrivateIp': each.get('PrivateIpAddress', ''),
            'InstanceId': each.get('InstanceId', ''),
            'SubnetId': each.get('SubnetId', ''),
            'VpcId': each.get('VpcId', ''),
            'InstanceName': get_tag(each, 'Name'),
            'volume.size': volsss['vol_size'],
            'volume.id': volsss['vol_id'],
            'volume.type': volsss['vol_type'],
            'DeleteOnTermination': each.get('DeleteOnTermination', ''),
            'SGGroupName': sgss['sg_name'],
            'SGGroupID': sgss['sg_id'],
            'State': each['State']['Name'],
            'Region': each['Placement']['AvailabilityZone']
        })


df = pd.DataFrame(result)
display(df)
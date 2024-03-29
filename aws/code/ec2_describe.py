
import boto3
import csv
import datetime
import logging
from os import environ
import collections
import time
import sys

# https://stackoverflow.com/questions/68765531/boto3-get-list-of-all-ec2-instances-with-ebs-volume-id-size-to-an-excel 
### ENABLE The profilename below, while testing from local. Disable this and session line in 63, enable line 64 session before pushing to Lambda#######
profilename='<>'
aws_Acct='<>.csv'
volume_id_list=[]
result = []
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
#regions = ['us-east-1']

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

def lambda_handler(event, context):
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info('EC2 Inventory details')

        for region in regions:
            session = boto3.Session(profile_name=profilename, region_name=region)
            #session = boto3.Session(region_name=region)
            ec2 = session.client('ec2')
            response = ec2.describe_instances()
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
                    
        # Write to csv file.
        header = ['ImageId', 'InstanceType', 'InstanceId', 'InstanceName', 'PublicIp', 'PrivateIp', 'Region', 'State', 'volume.id', 'volume.size', 'volume.type', 'SubnetId', 'VpcId', 'SGGroupName', 'SGGroupID', 'DeleteOnTermination']
        with open(aws_Acct, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(result)

    except Exception as e:
        logging.error(
            'EC2 inventory with uncaught exception: {}'.format(e)
        )

if __name__ == '__main__':
    lambda_handler(None, None)
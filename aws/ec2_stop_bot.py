# -*- coding: utf-8 -*-

import json
import boto3
from datetime import datetime, timedelta
from pprint import pprint 
import pandas as pd 

from IPython.display import display

######################################################################
# except
except_target = ['mfas-oregon-private-emr-dev', 'mfas-oregon-private-emr-qa', 'mfas-oregon-private-emr-prod']
except_target_tag = ['','']


# target ec2 state fileter
filters = [ 
    {
        'Name': 'instance-state-name', 
        'Values': ['running', 'stopped']
    }
]

# required tag
required_tag_list = ['Name' , 'Service' , 'Task' , 'Engine' , 'PG' , 'Env' , 'Batch' , 'EOS' ,  'E-Mail' ]


# target region
region_name = "us-west-2"

# pandas display
display_column = ['instance name', 'instance state', 'launch_time', 'required tag count', 'cpu max usage', 'action_type', 'E-mail', 'Phone', 'Batch', 'need tag list']
df_total = pd.DataFrame( columns = display_column )
######################################################################
## email or sms
target_arn = "arn:aws:sns:us-west-2:378010018656:mfas_EC2_check"
sns = boto3.client('sns', region_name='us-west-2')


def send_sns(email_addr, data):
    
    message = """
    Please Check your EC2  ======================================
    
    target EC2       :  {}  
    missing tag      :  {}
    max CPU usage    :  {}   ( 1시간 동안 max ) 
    
    EC2 will stop.
    
    =============================================================
    
    """.format( data[0], data[-1], data[4])
    
    response = sns.publish(
        TargetArn=target_arn,
        Subject = '[TEST][MON] EC2 테스트 메일입니다 내용 확인 부탁드립니다.',
        Message=json.dumps(
            {
                'default': str.encode(message, "utf-8").decode('utf8')
            }
        ),
        MessageStructure='json',

        MessageAttributes = {
            'email': {
                'DataType': 'String',
                'StringValue': email_addr
            }
        }
    )
    
    print("stop target : ".format(data[0]))

######################################################################




#ec2 = boto3.client('ec2', region_name=region_name)
cloudwatch = boto3.client('cloudwatch', region_name=region_name)

ec2_list = boto3.resource('ec2', region_name = region_name)

instances = ec2_list.instances.filter(Filters=filters)
instance_count = 0


for instance in instances:
    try:
        instance_count += 1 
        action_type = ''
        target_ec2_type = ''
        require_tag_count = 0
        total_tag_count = 0 
        tag_list = list()
        email = ''
        phone = ''
        batch = ''
        
        #### display 
        instance_name = 'empty name tag' 
        cpu_usage = 'Not Monitored'
        eos_date = 'Not Defined'
        
        #pprint(instance.tags)
        #pprint (instance) 
        
        # 1. tag 정보 조회  필요한 경우 조회 시점에 로직 적용 
        # tag의 key 값만 추출
        for i in range(len(instance.tags)):
            total_tag_count += 1 
            tag_list.append(instance.tags[i]['Key'].strip().lower())
            if instance.tags[i]['Key'] == 'Name':
                instance_name =  instance.tags[i]['Value'] 
            
            if instance.tags[i]['Key'] == 'E-Mail':
                email =  instance.tags[i]['Value']
                
            if instance.tags[i]['Key'] == 'Phone':
                phone =  instance.tags[i]['Value']
                
            if instance.tags[i]['Key'] == 'Batch':
                Batch =  instance.tags[i]['Value']   
            
            if instance.tags[i]['Key'] == 'aws:elasticmapreduce:job-flow-id':
                target_ec2_type = 'EMR'
        
        
        ################################################
        # 0. except target - emr 
        
        if instance_name in  except_target:
            # 상시 운영중인 EMR 제외
            continue
        if target_ec2_type == 'EMR':
            # transient 하게 구동 중인 EMR 제외 
            continue       
        
        
        
        ################################################
        # 1. 필수 tag가 적용되어 있지 않으면 action_type stop 으로 변경 ( 실제 value 에 대한 확인은 하지 않음 )
        tag_list = list(set(tag_list))
        need_tag_list = required_tag_list[:]
        # 1. requrired tag check
        for tag in tag_list:
            for require in required_tag_list:
                #print ( tag + '  :  ' + require.strip().lower())
                if tag.strip().lower() == require.strip().lower():
                    require_tag_count = require_tag_count + 1
                    need_tag_list.remove(require)
                
        if require_tag_count < len(required_tag_list) :
            action_type = 'stop'
        
        ################################################
        # 2. CPU max usage
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': instance.id
                },
            ],
            StartTime=datetime.now() - timedelta(seconds=3600),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=[
                'Maximum',
            ],
            Unit='Percent'
        )

        for cpu in response['Datapoints']:
            if 'Maximum' in cpu:
                
                cpu_usage = str(round(cpu['Maximum'] , 2) ) + "%" 
                if round(cpu['Maximum'] , 2) < 3  :
                    action_type= 'stop'
            else :
                action_type= 'monitoring cpu failed.'
                
        ################################################
        # 3. 예외 조치 사항
        # EMR 통해서 배치로 생성되는 EC2는 예외 조치 
        if Batch == 'O':
            action_type = ''
        
        fmt = '%Y-%m-%d %H:%M:%S'
        launch_time = datetime.strptime((instance.launch_time + timedelta(hours=9)).strftime(fmt), fmt)
        cur_time  = datetime.strptime((datetime.now() + timedelta(hours=9)).strftime(fmt), fmt)
        launch_delta = (cur_time - launch_time).total_seconds()/60/60
        #print(launch_delta/60/60)
        if launch_delta < 1:
            action_type = ''
        
        ################################################
        
        
        # logging display data
        add_row = [instance_name,  instance.state['Name'], launch_time, str(require_tag_count) + ' / '+ str(len(required_tag_list)),  str(cpu_usage), action_type, email, phone, Batch,  need_tag_list ]
        
        
        if action_type == 'stop':
            print ( action_type )
            #send_sns(email , add_row)
        
        df_total.loc[ instance_count ] = add_row 
            
        
    except Exception as e:
        print(e)
        
print("total instance count : " + str(instance_count))
pd.set_option("max_colwidth", 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', df_total.shape[0]+1)
display(df_total.sort_values(by=['instance state'], ascending=[True]).reset_index(drop=True))



    

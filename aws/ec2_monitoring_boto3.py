import json
import boto3
from datetime import datetime, timedelta
from pprint import pprint 
import pandas as pd 
from botocore.client import Config

from IPython.display import display

from pytz import timezone



'''
1) 태그가 제대로 안붙어 있는 instance는 launch 즉시 stop
- ec2 lanching trigger 

2) 자원 사용이 없는 instance는 주기적으로 스캔하여 stop, 담당자에게 notification 발송(메일 또는 sms)
- time schedule ( daily? )

3) 모든 instance는 LastLaunchDTTM(마지막 start 시점) + 3개월로 EOS 일자 자동 지정 + EOS 일자
- time schedule ( daily )


4) EOS 일자가 지나면 Termination Tag에 "O" flag을 담
- time schedule


5) 매주 일요일 Termination Tag가 "O"인 instance를 자동으로 Termination
    ※ AWS Backup에 Termination Tag가 "O"인 instance을 자동으로 backup 하는 Rule 구성ZZ
- time schedule ( weekly )

'''

######################################################################
# 예외 대상
except_target = ['mfas-oregon-private-emr-dev', 'mfas-oregon-private-emr-qa', 'mfas-oregon-private-emr-prod']

# 대상 필터
filters = [ 
    {
        'Name': 'instance-state-name', 
        'Values': ['running', 'stopped']
    }
]

# 필수 태그 정리 
#required_tag_list = [ 'E-Mail', 'EOS', 'Env']
required_tag_list = ['Name' , 'Service' , 'Task' , 'Engine' , 'PG' , 'Env' , 'Batch' , 'EOS' ,  'E-Mail']


# target region
region_name = "us-west-2"
#region_name = "ap-northeast-2"

# pandas display
display_column = ['instance name', 'type', 'instance state', 'required tag count', 'total tag count', 'cpu max usage', 'Last launch time', 'EOS Date', 'Taged EOS', 'Termination Tag', 'action_type', 'E-mail', 'Phone', 'Batch', 'need tag', 'tag_list']
df_total = pd.DataFrame( columns = display_column )
######################################################################

config = Config(connect_timeout=20000, read_timeout=20000)


#ec2 = boto3.client('ec2', region_name=region_name)
cloudwatch = boto3.client('cloudwatch', region_name=region_name, config=config)

ec2_list = boto3.resource('ec2', region_name = region_name, config=config)
# running중인 Instance 추출
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
        batch = 'X'
        
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
            
            if instance.tags[i]['Key'] == 'EOS':
                eos_date =  instance.tags[i]['Value']
                
            if instance.tags[i]['Key'] == 'E-Mail':
                email =  instance.tags[i]['Value']
                
            if instance.tags[i]['Key'] == 'Phone':
                phone =  instance.tags[i]['Value']
            
            if instance.tags[i]['Key'] == 'Batch':
                batch =  instance.tags[i]['Value']
            
            
            # Termination Tag가 있는 경우 처리 
            if instance.tags[i]['Key'] == 'Termination' and instance.tags[i]['Value'] == 'O':
                action_type = 'terminate'
            
            # 예외 로직 
            if instance.tags[i]['Key'] == 'aws:elasticmapreduce:job-flow-id':
                target_ec2_type = 'EMR'
        
        
        ################################################
        # 상시 예외 처리 - emr 
        if instance_name in  except_target:
            continue
        if target_ec2_type == 'EMR':
            # transient 하게 구동 중인 EMR 제외 
            continue  
        
        
        # ec2 사용 목적에 따라 분류 혹은 예외 처리 
        if target_ec2_type == 'EMR':
            ec2_type = 'EMR'
        else :
            ec2_type = 'EC2'
        
        
        
        
        ################################################
        # 필수 tag 유무 판별   
        # 반복된 key 제거
        tag_list = list(set(tag_list))
        need_tag_list = required_tag_list[:]
        for tag in tag_list:
            for require in required_tag_list:
                #print ( tag + '  :  ' + require.strip().lower())
                if tag.strip().lower() == require.strip().lower():
                    require_tag_count = require_tag_count + 1
                    need_tag_list.remove(require)
        
        if require_tag_count < len(required_tag_list) :
            #print("필수 tag가 부족한 EC2 (not enough tag) :  " + instance_name + '  -  ' + instance.id)
            action_type = 'stop'
        
        ################################################
        # CPU max 사용률 확인 
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
                #print(instance.id,"의 1시간 최대 CPU 사용률 : ",cpu['Maximum'],"%")
                cpu_usage = str(round(cpu['Maximum'] , 2) ) + "%" 
                if round(cpu['Maximum'] , 2) < 5:
                    action_type= 'stop'
            else :
                action_type= 'stop'
        
        ################################################
        # 최종 예외 처리 
        if batch =='O':
            action_type = ''
        
        ################################################
        
        
        # last launch time 
        launch_time = instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
        cur_time  = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        
        
        ################################################
        # EOS 확인 
        # 태그 기준과 계산 기준 중 어느것으로 적용할지 확인 
        
        EOS_date = (instance.launch_time + timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        
        #print ( EOS_date )
        #print ( cur_time ) 
        
        
        ################################################
        # termination tag 설정 
        # 매주 일요일에 실제 적용
        if cur_time > EOS_date:
            Termination_tag = 'O'
            action_type = 'Termination'
        else:
            Termination_tag = 'X'
        
        if action_type == 'stop' and instance.state['Name'] != 'running' :
            action_type = ''
        
        '''
        # action 유형별 실행             
        if action_type == 'terminate':
            print('Action. terminate : ' + instance_name )
        elif action_type == 'stop':
            print('Action. stop  : ' + instance_name )
        else:
            print('Action. nothing')
        print ( '-------------------------------------------------------------------------------------------------------')
        print ( '0. instance name        : ' + instance_name )
        print ( '1. instance state       : ' + instance.state['Name']  )
        print ( '2. required tag count   : ' + str(require_tag_count) + ' / '+ str(len(required_tag_list)) + '  -  total tag count : ' + str(total_tag_count))
        print ( '3. cpu max usage        : ' + str(cpu_usage))
        print ( '4. Last launch time     : ' + launch_time )
        
        print ( '5. EOS Date             : ' + EOS_date + ' /  Taged EOS date : ' + eos_date  )
        print ( '6. Terminate Tag        : ' + Terminate_tag )
        print ( '7. action_type          : ' + action_type )
        
        print('\n')
        '''
        
        add_row = [instance_name, ec2_type,  instance.state['Name'], str(require_tag_count) + ' / '+ str(len(required_tag_list)),  str(total_tag_count), str(cpu_usage), launch_time , EOS_date, eos_date, Termination_tag, action_type, email, phone, batch,  need_tag_list, tag_list ]
        
        df_total.loc[ instance_count ] = add_row 
        
        
        #add_serise = pd.Series(add_row, index = display_column ) 
        #print ( add_serise)
        #df_total.append( add_serise, ignore_index = True )
        
        
    except Exception as e:
        print(e)
        
print ( "total instance count : " + str(instance_count))
pd.set_option("max_colwidth", 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', df_total.shape[0]+1)



display(df_total.sort_values(by=['instance state', 'Last launch time'], ascending=[True, False]).reset_index(drop=True))

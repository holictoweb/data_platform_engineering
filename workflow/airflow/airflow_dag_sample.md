# AIRFLOW 기능 확인

1. [RestAPI 로 Dag 호출](#1. RestAPI 로 Dag 호출)
   1. [RestAPI용 User 생성](#1. RestAPI용 User 생성)
   2. [RestAPI로 Dag 호출](#2. RestAPI로 Dag 호출)
2. [S3 Data Sync](#2. S3 Data Sync)
3. [Airflow variable 내용 Json으로 읽기](#3. Airflow variable 내용 Dict로 읽기)
4. [조건에 부합하는 Task만 수행하고 그 외의 Task는 Skip](#4. 조건에 부합하는 Task만 수행하고 그 외의 Task는 Skip)
5. [Dag에서 외부 Dag trigger 및 감지](#5. Dag에서 외부 Dag trigger 및 감지)
6. [특정 시점에 Task가 실행 되도록 Pending](#6. 특정 시점에 Task가 실행 되도록 Pending)

---

## 1. RestAPI 로 Dag 호출

### 1. RestAPI용 User 생성

목적 : RestAPI 로 Dag 호출
airflow cli 또는 airflow UI에서 생성한 User는 airflow Web service 이용을 위한 User 입니다.
RestAPI로 Dag에 접근하기 위해서는 RestAPI 용 User 생성을 해야합니다.

```python
# airflow rest api user create

from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
# User Info
user.username = 'jungmin'
user.email = 'jungmin.choi@partner.sec.co.kr'
user.password = '1234'
session = settings.Session()
user_exists = session.query(models.User.id).filter_by(username=user.username).scalar() is not None
if not user_exists:
    session.add(user)
    session.commit()
session.close()

```

### 2. RestAPI로 Dag 호출

위에서 생성한 User Info를 가지고 RestAPI 호출

```python
import requests
import json
from pprint import pprint

username = 'jungmin'
password = '1234'

result = requests.post(
  "http://{Master_Private_IP}:8080/api/experimental/dags/{DAG_NAME}/dag_runs",
  data=json.dumps("{}"),
  auth=(username, password))
pprint(result.content.decode('utf-8'))

```

해당 내용을 적용하기 위해서는 Master server에 대한 8080 Port가 Open 되어야 합니다.

## 2. S3 Data Sync

목적 : S3 `mfas-data-warehouse`의 Prod Data를 QA에 Sync

```python
# 1. Cluster Info 조회
# 2. Prod Data를 QA에 Sync하는 Step 추가
# 3. Step Sensor
# 4. 이전 Task 상태가 Fail 인 경우 RestAPI로 Dag 다시 실행
from airflow import DAG
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import DagBag
from datetime import datetime, timedelta
from airflow.models import TaskInstance
from airflow.models import Variable
import requests
import json
import time
import os
import boto3
from pprint import pprint
import logging

log = logging.getLogger(__name__)

#########################################################################
# parameter settings
#########################################################################

DAG_NAME = 'S3_Data_Sync_Workflow'
EMR_CLUSTER_TASK_ID='get_cluster_id'
aws_conn_id='aws_oregon'
emr_conn_id='emr_default'
# RestAPI User Info From Variable
username = Variable.get("JUNGMIN-NAME")
password = Variable.get("JUNGMIN-PASS")
# AIRFLOW ENV Check From Variable (prod or dev)
ENV = Variable.get("ENV")

#########################################################################
# Default config settings
#########################################################################

default_args = {
    'owner': 'mfas.manage',
    'depends_on_past': False,
    'start_date': datetime(2021,2,22),
    'provide_context' : True,
    'max_active_runs' : 30
}

# 새벽 6시에 수행
dag = DAG(DAG_NAME,
    default_args=default_args,
    schedule_interval= '0 6 * * *',
    catchup=True,
    concurrency = 30,
    tags=[
        ENV,
        "EMR_MANAGEMENT"
    ]
)

# Get Cluster Info
def get_cluster_id(**kwargs):
    client = boto3.client('emr',  region_name='us-west-2')
    # 실행 중인 cluster 정보 모두 조회
    response = client.list_clusters(
        CreatedAfter=datetime(2020, 1, 1),
        CreatedBefore=datetime(2099, 1, 1),
        ClusterStates=[
            'WAITING','RUNNING'
        ]
    )
    index = 0
    for key in response['Clusters']:
        res = client.describe_cluster(ClusterId=key['Id'])
        name = res['Cluster']['Name']
        name = name.lower()
        # 조회한 cluster 정보 중 이름이 같은 Cluster의 ID를 Xcom으로 Push
        if 'mfas-oregon-private-emr-' + ENV in name:
            print(name)
            print(key['Id'])
            kwargs['ti'].xcom_push(key='jobflow_id', value=key['Id'])

# 특정 Task의 상태를 확인 후 restAPI로 Dag 재수행
def call_external_dag(**kwargs):
    # 실행 날짜 획득
    execution_date = kwargs['execution_date']
    # Dag 정보 획득
    dag_instance = kwargs['dag']
    # 특정 Task 정보 조회
    operator_instance = dag_instance.get_task("prod_to_qa_checker")
    # Task 상태 조회
    task_status = TaskInstance(operator_instance, execution_date).current_state()
    if task_status == 'failed':
        # Trigger Dag with REST API
        result = requests.post(
            "http://localhost:8080/api/experimental/dags/" + DAG_NAME + "/dag_runs",
            data=json.dumps("{}"),
            auth=(username, password))
        pprint(result.content.decode('utf-8'))
    else:
        pprint(task_status)

get_cluster_id = PythonOperator(
    task_id='get_cluster_id',
    provide_context=True,
    python_callable=get_cluster_id,
    dag=dag,
)

# data-warehouse의 Prod data 를 Qa로 Sync
prod_to_qa = EmrAddStepsOperator(
    task_id='prod_to_qa',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='get_cluster_id', key='jobflow_id') }}",
    aws_conn_id=aws_conn_id,
    steps=[
            {
                'Name': 'prod_to_qa',
                'ActionOnFailure': 'CONTINUE',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        "aws", 
                        "s3",
                        "sync",
                        "s3://mfas-data-warehouse/prod/", 
                        "s3://mfas-data-warehouse/qa/",
                        "--delete",
                        "--no-verify-ssl"
                    ]
                }
            }
        ],
    default_args=default_args,
    trigger_rule='all_done',
    retries=30,
    dag=dag
)

prod_to_qa_checker = EmrStepSensor(
    task_id = 'prod_to_qa_checker',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='get_cluster_id', key='jobflow_id') }}",
    step_id="{{ task_instance.xcom_pull(task_ids='prod_to_qa', key='return_value')[0] }}",
    aws_conn_id=aws_conn_id,
    trigger_rule='all_done',
    retries=30,
    dag=dag
)

retry_dag = PythonOperator(
    task_id='retry_dag',
    provide_context=True,
    python_callable=call_external_dag,
    trigger_rule='all_done',
    dag=dag
)

dummy_job = DummyOperator(task_id='dummy_job', dag=dag)

#########################################################################
# Design DAG
#########################################################################

get_cluster_id >> prod_to_qa >> prod_to_qa_checker >> retry_dag >> dummy_job
```

## 3. Airflow variable 내용 Dict로 읽기

목적 : Airflow에서 EMR 생성에 필요한 Config 내용을 Variable로 저장
해당 Variable을 Dict 형태로 조회후 사용

유의 사항 : Variable에 Dict 형태로 저장을 해도 Code 상에서 변수를 Load하면 String type으로 반환

Varialbe 저장 예시 

````json
{
        "mfas_workflow_SDC_FCST": "j-1GM824UZAT1O6",
        "mfas_workflow_PSIWARNING_INBOUND": "j-3DTEH9LBPN9ZS",
        "mfas_workflow_SEA_AI_FCST_RDC_PART1": "j-2QR2K8WBWWFDR",
        "mfas_workflow_RDC_FCST": "j-1USPZ03IBY8PD",
        "mfas_workflow_GSBN_INBOUND_1210": "j-32XBT2F7HDK0H",
        "mfas_workflow_GSBN_INBOUND_0940": "j-23SI6M921F7LC",
        "mfas_workflow_SDC_FCST_WED_0330": "j-1XIZBIBMIC9JY",
        "mfas_workflow_INF_10_190_Create_Send_Data_GSCM": "j-ACMUK80ZYFUH",
        "mfas_workflow_Batch_MoTu_1240_RTF_PRICE": "",
        "mfas_workflow_Batch_Tue_1230_Promotion_Cores": "",
        "mfas_workflow_Batch_Fri_0600_LocalPromo": ""
}
````

실제 반환 값

```json
'{"mfas_workflow_SDC_FCST": "j-1GM824UZAT1O6", "mfas_workflow_PSIWARNING_INBOUND": "j-3DTEH9LBPN9ZS", "mfas_workflow_SEA_AI_FCST_RDC_PART1": "j-2QR2K8WBWWFDR", "mfas_workflow_RDC_FCST": "j-1USPZ03IBY8PD", "mfas_workflow_GSBN_INBOUND_1210": "j-32XBT2F7HDK0H", "mfas_workflow_GSBN_INBOUND_0940": "j-23SI6M921F7LC", "mfas_workflow_SDC_FCST_WED_0330": "j-1XIZBIBMIC9JY", "mfas_workflow_INF_10_190_Create_Send_Data_GSCM": "j-ACMUK80ZYFUH","mfas_workflow_Batch_MoTu_1240_RTF_PRICE":"","mfas_workflow_Batch_Tue_1230_Promotion_Cores":"","mfas_workflow_Batch_Fri_0600_LocalPromo":""}'
```

호출 방법

```python
from airflow.models import Variable
from ast import literal_eval
import json

# 상단에 import한 내용으로 호출하면 됩니다.
EMR_CLUSTER_TASK_ID = literal_eval(Variable.get("CLUSTER-ID"))
EMR_CLUSTER_TASK_ID = json.loads(Variable.get("CLUSTER-ID"))
```

## 4. 조건에 부합하는 Task만 수행하고 그 외의 Task는 Skip

`ShortCircuitOperator` , `AirflowSkipException` 을 이용하면 Codition에 따라 해당 task의 하위 task들에 대해 skip을 시킬 수 있습니다.

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import os
from airflow.models import Variable
MODULE_PATH = Variable.get("MODULE-PATH")
import sys
sys.path.append(MODULE_PATH)
from run_cf_module import *
from airflow.operators.python_operator import ShortCircuitOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta
import time

#############################################################################
# User parameter settings
#############################################################################
pg_name = 'shorcircuitoperator_test'
current_time = check_current_time()
dag_id = pg_name+'_'+current_time
user = 'mfas_Airflow'

#############################################################################
# DAG & operator definition
#############################################################################

DAG_NAME = 'mfas_run_cf_{}'.format(pg_name)
aws_conn_id='aws_oregon'
emr_conn_id='emr_default'

default_args = {
    'owner': 'jungmin.choi',
    'depends_on_past': False,
    'start_date': datetime(2021,2,22),
    'provide_context' : True,
    'max_active_runs' : 30
}

dag = DAG(DAG_NAME,
    default_args=default_args,
    schedule_interval= None,
    catchup=False,
    concurrency = 10
)

# task a, c, f 에서 시간을 확인하고 true 일 경우에만 하위 task가 진행 됩니다.
task_a_time = "08:51"
task_c_time = "08:51"
task_f_time = "08:51"

# 조건을 제시해줄 함수 입니다.
# 현재 시간과 실행해야할 시간이 일치하면 True 그 외에는 False를 반환 합니다.
def get_time(time, check_time):
    time = str(time).split("+")[0]
    dt_time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=9) + timedelta(minutes=1)
    print(dt_time)
    print(dt_time.strftime("%H:%M:%S"))
    return dt_time.strftime("%H:%M") == check_time

# task a, c, f 에서 시간을 확인하여 일치하면 True 그 외에는 Exception 처리합니다.
def task_a_check_time(**kwargs):
    if get_time(kwargs['execution_date'], task_a_time):
        return True
    else:
        raise AirflowSkipException("Skip this task and individual downstream tasks while respecting trigger rules.")

def task_c_check_time(**kwargs):
    if get_time(kwargs['execution_date'], task_c_time):
        return True
    else:
        raise AirflowSkipException("Skip this task and individual downstream tasks while respecting trigger rules.")

def task_f_check_time(**kwargs):
    if get_time(kwargs['execution_date'], task_f_time):
        return True
    else:
        raise AirflowSkipException("Skip this task and individual downstream tasks while respecting trigger rules.")

# ShortCircuitOperator 는 PythonOperator처럼 사용 가능
# 단 return 값이 True or False
# True 일 경우 하위 task 계속 진행
# False 일 경우 하위 task 모두 skip
task_A = ShortCircuitOperator(
    task_id = 'task_A',
    python_callable = task_a_check_time,
    provide_context = True,
    dag = dag
)

task_C = ShortCircuitOperator(
    task_id = 'task_C',
    python_callable = task_c_check_time,
    provide_context = True,
    dag=dag,
    trigger_rule='none_failed'
)

task_F = ShortCircuitOperator(
    task_id = 'task_F',
    python_callable = task_f_check_time,
    provide_context = True,
    dag=dag
)
 
task_B = DummyOperator(task_id = 'task_B', dag = dag, depends_on_past = False)
task_D = DummyOperator(task_id = 'task_D', dag = dag, depends_on_past = False)
task_E = DummyOperator(task_id = 'task_E', dag = dag)
task_G = DummyOperator(task_id = 'task_G', dag = dag, depends_on_past = False)

task_A >> task_B >> task_C >> task_D >> task_E
task_F >> task_G
```

## 5. Dag에서 외부 Dag trigger 및 감지

Dag 내부 task에서 외부 Dag trigger 및 task 수행 여부 감지

```python
# 외부 Dag trigger
from airflow.operators import TriggerDagRunOperator
# 외부 Dag task sensor
from airflow.sensors.external_task_sensor import ExternalTaskSensor

# Trigger 대상 Dag id 작성
# execution_date : 현재 execution_date를 받아옴
trigger_test = TriggerDagRunOperator(
    task_id="trigger_test",
    trigger_dag_id="jungmin_func_test",
    execution_date="{{ execution_date }}",
    dag=dag
)

# external_dag_id : sensor 대상 dag id
# external_task_id : sensor 대상 task id (dag 전체를 감지하고 싶다면 마지막 task id 또는 None 표시)
# execution_date_fn : 현재 execution_date를 받아옴
# timeout : sensor timeout
waiting_extract_dag = ExternalTaskSensor(
    task_id='waiting_extract_dag',  # waiting for the whole dag to execute
    external_dag_id='jungmin_func_test',  # here is the id of the dag
    external_task_id='push_time',  # waiting for the whole dag to execute 
    execution_date_fn=lambda dt: dt,
    dag=dag,
    execution_timeout=timedelta(minutes=30),
    timeout=7200,
)
```

## 6. 특정 시점에 Task가 실행 되도록 Pending

특정 시점이 될 때까지 task에서 pending 후 특정 시점이 되면 하위 task들 진행

```python
from airflow.operators.python_operator import PythonOperator

# execution_time 설정
execution_time = "12:40"

def wait_time(**kwargs):
    while True:
        cur_time = (datetime.now()).strftime("%H:%M")
        # 현재 시점이 수행할 시점과 일치한다면
        if cur_time == execution_time:
            break
        else:
            # 1분씩 대기하며 pending
            print('Poking for {} on {} ... '.format(kwargs['task_instance_key_str'], cur_time))
            time.sleep(60)
            

wait_time = PythonOperator(
    task_id = 'wait_time',
    python_callable = wait_time,
    provide_context = True,
    dag=dag
)
```



## ssh operator
- connector 를 사용 하여 연결 설정 후 EMR에 있는 python 스크립트 수행 
```python
def EMR_ssh_conn(connid,bash_command,dag):
    sshHook = SSHHook(connid)
    ssh_operator = SSHOperator(
        ssh_hook=sshHook,
        task_id=connid,
        command=bash_command,
        dag=dag
    )
    return ssh_operator

ec2_stop_task = EMR_ssh_conn('dev_emr_ssh_conn','python3 /home/hadoop/management/mng_ec2_stop_10min.py',dag)
```


## trigger dag
- retry 를 위해 실패 시 다시 dag 수행 
```python
# Get Task Statue & rest api call external dag
def call_external_dag(**kwargs):
    # Get execution_date
    execution_date = kwargs['execution_date']
    # Get Dag & Task Info
    dag_instance = kwargs['dag']
    operator_instance = dag_instance.get_task("check_prod_to_qa_s3_sync")
    # Task Status
    task_status = TaskInstance(operator_instance, execution_date).current_state()
    if task_status == 'failed':
        # Trigger Dag with REST API
        # result = requests.post(
        #     "http://{}:8080/api/experimental/dags/".format(airflow_master_node_ip) + DAG_NAME + "/dag_runs",
        #     data=json.dumps("{}"),
        #     auth=(airflow_sys_user_id, airflow_sys_user_pwd))
        # pprint(result.content.decode('utf-8'))
        c = Client(None, None)
        c.trigger_dag(dag_id=DAG_NAME, run_id='triggering_rerty_logic_{}'.format(current_time), conf={})
    else:
        pprint(task_status)

retry_logic = PythonOperator(
    task_id='retry_logic',
    provide_context=True,
    python_callable=call_external_dag,
    trigger_rule='all_done',
    dag=dag
)
```

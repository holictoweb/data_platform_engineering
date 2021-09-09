
import boto3
import os
from datetime import timedelta
import datetime

import pymysql
import pandas as pd

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.operators.python import PythonOperator

# dummy
from airflow.operators.dummy import DummyOperator

# 분기를 위한 operator 
from airflow.operators.python import BranchPythonOperator

# ecs 용 operator 
# sample : https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_modules/airflow/providers/amazon/aws/example_dags/example_ecs_fargate.html
from airflow.providers.amazon.aws.operators.ecs import ECSOperator

# task group 생성
from airflow.utils.task_group import TaskGroup

# variable 사용 
from airflow.models.variable import Variable




'''
# dag 반영 
python3 -c "from airflow.models import DagBag; d = DagBag();"
'''



dag = DAG(
    dag_id="[workflow]DEV_aicel_crawling_nlp",
    default_args={
        "owner": "aicel",
        "depends_on_past": False,
    },
    default_view="graph",
    #schedule_interval='0 */1 * * *',
    schedule_interval=None,
    start_date=datetime.datetime(2021, 9, 1),
    tags=["dev", "ecs", 'pipeline'],
)

# generate dag documentation
dag.doc_md = __doc__
dag.doc_md = """
### test
what!!!!!
"""


################################## variables
con_cnt = Variable.get("fargate_crawling_ecs_container_cnt")
AIRFLOW_ECS_OPERATOR_RETRIES = 2


################################## python function

start_task = DummyOperator( task_id = 'start_task', dag=dag)
end_task = DummyOperator( task_id = 'task_all_done', dag=dag)

# print(df_crawling_jobs)
'''
for idx, row in df_crawling_jobs.iterrows():    
    dummy_ecs_crawling = DummyOperator( task_id = 'task_crawling_job_' + row['company_code'] , dag=dag)
    #end_company_task = DummyOperator( task_id = 'end_company_task' + row['company_code'] , dag=dag)

    df_nlp_jobs_pre = df_nlp_jobs[df_nlp_jobs['company_code']==row['company_code']]
    if df_nlp_jobs_pre.empty == False:
        nlp_group_name = 'nlp_group_' +  row['company_code']
        with TaskGroup(nlp_group_name, dag=dag) as nlp_group:
            for jdx, row_nlp in df_nlp_jobs_pre.iterrows():
                dummy_ecs_nlp = DummyOperator( task_id = 'task_nlp_job_' + row_nlp['company_code'] + '_' + row_nlp['news_url_md5'] , dag=dag)
            
        start_task >> dummy_ecs_crawling >> nlp_group  >> end_task
    else:
        start_task >> dummy_ecs_crawling >> end_task

    
    if idx == 10:
        break
network_configuration={
            "awsvpcConfiguration": {
                "subnets": [os.environ.get("SUBNET_ID", "subnet-246db769")],
            },
        },

    awslogs_group="/ecs/dev-task-definition-01",
    awslogs_stream_prefix="ecs/", 
'''



for i in range(int(con_cnt)):
    esc_taske = ECSOperator(
        task_id="airflow_task_dev_container_task_" + str(i) ,
        dag=dag,
        aws_conn_id="aws_default",
        region_name="ap-northeast-2",
        task_definition="dev-task-definition-01",
        cluster="dev-aicel-cluster",
        launch_type="FARGATE",
        overrides={
            "containerOverrides": [
                {
                    "name": "dev-task-definition-01",
                    "command": ["python", "/app/test.py"],
                    
                },
            ],
        },
        network_configuration={
            "awsvpcConfiguration": {
                "assignPublicIp" : "ENABLED",
                "subnets": [os.environ.get("SUBNET_ID", "subnet-246db769")],
            },
        },
        tags={
            "Owner": "airflow",
            "Environment": "Development",
        },
        awslogs_group="/ecs/dev-task-definition-01",
        awslogs_stream_prefix="ecs/dev-task-definition-01", 
        retries = AIRFLOW_ECS_OPERATOR_RETRIES,
        retry_delay = timedelta(seconds=10)

    )

    start_task >> esc_taske >> end_task



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

'''
# dag 반영 
python3 -c "from airflow.models import DagBag; d = DagBag();
'''



dag = DAG(
    dag_id="aicel_ecs_fargate_dag",
    default_args={
        "owner": "aicel",
        "depends_on_past": False,
    },
    default_view="graph",
    schedule_interval='*/30 * * * *',
    start_date=datetime.datetime(2021, 9, 1),
    tags=["example", "ecs"],
)

# generate dag documentation
dag.doc_md = __doc__
dag.doc_md = """
### aicel test dag
ecs 테스트용도 

1. mysql 상에 gn_news_nlp_job 기반으로 수행 하고자 하는 대상 선정
2. ecsoperator 를 사용하여 해당 작업 수행 
"""

################################## python function
def get_gn_news_job():
    connection = pymysql.connect(host='fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
                                user='mi_ro',
                                password='aicel2021!',
                                database='news',
                                cursorclass=pymysql.cursors.DictCursor)

    # connect 에서 cursor 생성
    cursors = connection.cursor()

    # SQL문 실행
    sql = "select * from news.ncc_news_job where flag='0'"
    cursors.execute(sql)

    # data fetch
    data = cursors.fetchall()
    #print(data)
    # connection 닫기
    connection.close()
    
    return data

def get_gn_news_nlp_job():
    connection = pymysql.connect(host='fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
                                user='mi_ro',
                                password='aicel2021!',
                                database='news',
                                cursorclass=pymysql.cursors.DictCursor)

    # connect 에서 cursor 생성
    cursors = connection.cursor()

    # SQL문 실행
    sql = "select * from news.ncc_news_mapping"
    cursors.execute(sql)

    # data fetch
    data = cursors.fetchall()
    #print(data)
    # connection 닫기
    connection.close()
    
    return data 


################################## operators
start_task = DummyOperator( task_id = 'start_task', dag=dag)
end_task = DummyOperator( task_id = 'task_all_done', dag=dag)


crawling_list = get_gn_news_job()
df_crawling_jobs = pd.DataFrame(crawling_list)


nlp_list = get_gn_news_nlp_job()
df_nlp_jobs = pd.DataFrame(nlp_list)


# print(df_crawling_jobs)

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

    if idx == 3:
        break





'''
hello_world = ECSOperator(
    task_id="hello_world",
    dag=dag,
    aws_conn_id="aws_default",
    region_name="ap-northeast-2",
    task_definition="hello-world",
    cluster="c",
    launch_type="FARGATE",
    overrides={
        "containerOverrides": [
            {
                "name": "hello-world-container",
                "command": ["echo", "hello", "world"],
            },
        ],
    },
    network_configuration={
        "awsvpcConfiguration": {
            "securityGroups": [os.environ.get("SECURITY_GROUP_ID", "sg-123abc")],
            "subnets": [os.environ.get("SUBNET_ID", "subnet-123456ab")],
        },
    },
    tags={
        "Customer": "X",
        "Project": "Y",
        "Application": "Z",
        "Version": "0.0.1",
        "Environment": "Development",
    },
    awslogs_group="/ecs/hello-world",
    awslogs_stream_prefix="prefix_b/hello-world-container",  # prefix with container name
    )


start_task >> job_list >> end_task
'''
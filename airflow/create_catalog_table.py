from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator

from airflow.executors.local_executor import LocalExecutor

import boto3
from pprint import pprint
from pyhive import hive


DEFAULT_ARGS = {
    'owner': 'mfas',
    'depends_on_past': False,
    'start_date': days_ago(3)
}



dag = DAG(
    'mng_catalog_table',
    default_args=DEFAULT_ARGS,
    schedule_interval= None,
    catchup=False,
    concurrency = 10,
    tags=[
        "manage",
        "dev"
    ]
)

import boto3
from pprint import pprint
import boto3
from datetime import timedelta, datetime, timezone

##########################################
host_name = "172.17.8.142"
port = 10001
user = "hadoop"
database="mfas_lji_test"

op_mode = 'qa'
##########################################
    

def create_catalog_table( s3_location, cur):
    try:
        table_name = s3_location.split('/')[-2]
        table_name = table_name.replace('.', '_')
        drop_sql = 'drop table if exists `'+ database +'`.`' + table_name +'`'
        cur.execute(drop_sql)
        create_sql = 'create table `' + database  + '`.`' + table_name + '` using org.apache.spark.sql.parquet options ( path "' + s3_location  + '" , fileFormat "PARQUET")'
        cur.execute(create_sql)
        #print ( create_sql)
        print ( table_name + 'create completed')
    except Exception as e :
        print( e)


def manage_catalog():
    
    prefix = '{op_mode}/'.format(op_mode=op_mode)
    S3Targets = []
    target_bucket = 'mfas-data-warehouse'
    
    
    targate_date = datetime.now(timezone.utc) + timedelta(hours=-9) - timedelta(days=1)

    conn = hive.Connection(host=host_name, port=port, username=user, database=database)
    cur = conn.cursor()
        
    s3_client = boto3.client('s3')
    paginator = boto3.client('s3').get_paginator('list_objects')
    
    
    iterator = paginator.paginate(Bucket=target_bucket, Prefix=prefix, Delimiter='/', PaginationConfig={'PageSize': None})
    for response_data in iterator:
        prefixes = response_data.get('CommonPrefixes', [])
        for prefix in prefixes:
            prefix_name = prefix['Prefix']
            
            s3target = "s3://{bucket}/{tb}".format(bucket=target_bucket,tb = prefix_name)
            S3Targets.append(s3target)
            
            response = s3_client.list_objects_v2(Bucket= target_bucket, Prefix=prefix_name)
            
            
            for object in response['Contents']:
                #print (type(object['LastModified']))
                if object['LastModified'] > targate_date :
                    print(s3target)
                    print(object['Key'])
                    print(object['LastModified'])
                    create_catalog_table(s3target, cur)
                    break
            
    conn.close()        
    #pprint(S3Targets)
    pprint(len(S3Targets))


t1 = PythonOperator(
    task_id ="manage_catalog",
    python_callable= manage_catalog,
    dag=dag
)

t1

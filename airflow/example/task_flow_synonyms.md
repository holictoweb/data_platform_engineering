

# task flow 예제

```python

import json
from datetime import datetime

from airflow.decorators import dag, task

from IPython.display import display

import pymysql
from pprint import pprint 
import logging

'''
# dag 반영 
python3 -c "from airflow.models import DagBag; d = DagBag();"
'''

################################################ variables
# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)



news_con = pymysql.connect(host='fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
                user='admin',
                password='finance2016!',
                database='news',
                cursorclass=pymysql.cursors.DictCursor)
                
fngo_con = pymysql.connect(host='bigfinance-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
            user='fngo',
            password='fngofinance',
            database='fngo',
            cursorclass=pymysql.cursors.DictCursor)




################################################ dags

@dag(schedule_interval=None, start_date=datetime(2021, 1, 1), catchup=False, tags=['example'])
def task_batch_company_synonyms():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    @task()
    def get_bigfinance_company():
        # mysql 연결 데이터 확인
        # fngo database 연결 
        

        
        fngo_query = '''
        select * from fngo.company
        where is_trading = 1 
            AND company_code NOT IN (
                SELECT company_code FROM company_filters
                WHERE company_code NOT IN ( SELECT company_code FROM company_whitelist )
            );
        '''

        news_query = '''
        select * from news.gn_company_keywords
        where auto_flag = 1 ;
        '''

        try:
            fngo_cur = fngo_con.cursor()
            fngo_cur.execute(fngo_query)
            res = fngo_cur.fetchall()
            df_fngo = pd.DataFrame(res)
            
            news_cur = news_con.cursor()
            news_cur.execute(news_query)
            res = news_cur.fetchall()
            df_news = pd.DataFrame(res)
            
            print('>> fngo data')
            display(df_fngo.head(10))
            print('>> news data')
            display(df_news.head(10))
        except Exception as e:
            print(e)
        finally:
            fngo_cur.close
            news_cur.close
            news_con.close
            fngo_con.close

        logger.info(f">>> fngo total data : {len(df_fngo)}")
        
        return df_fngo

    @task(multiple_outputs=True)
    def compare_data(order_data_dict: dict):
        df_pivot = df_fngo.loc[:,['company_code', 'company_name', 'company_name_eng']]
        df_pivot['corp_code'] = df_fngo.company_code.str[1:]
        # display(df_pivot.head(10))
        print(f'total input : {len(df_pivot)}')

        df_pivot = df_pivot.melt( id_vars='company_code', var_name= 'keyword_type', value_name= 'keyword')
        # display(df_pivot.loc[(df_pivot.company_code == 'A000210' )])
        print(f'total pivot : {len(df_pivot)}')

        # table 저장된 데이터 존재 시

        df_update = pd.DataFrame()
        df_delete = pd.DataFrame()
        if df_news.empty == False:
            df_check = df_news[['company_code', 'keyword_type', 'keyword']] 
            # df_update = df_pivot.merge(df_check, how = 'inner' ,indicator=False)
            # df_update = pd.concat([df_check,df_pivot]).drop_duplicates(keep=False)
            
            df_update=pd.merge(df_pivot,df_check,how="outer",indicator=True)
            # display(df_update)
            df_update=df_update[df_update['_merge']=='left_only']
            df_delete=df_update[df_update['_merge']=='right_only']
            
            # display(df_check.loc[df_check.company_code == 'A039570'])
            # display(df_pivot.loc[df_pivot.company_code == 'A039570'])

        else:
            df_update = df_pivot

        display(df_update)
        display(df_delete)


        return {"df_update": df_update, "df_delete":df_delete}

    @task()
    def transform(df_update: dict, df_delete: dict):
        # fngo에 있는 신규 데이터만 추가 insert 
        try:
            news_cur = news_con.cursor()
            if df_update.empty == False:
                for idx, row in df_update.iterrows():
                    # print(row)
                    # Create a new record
                    if "_merge" in row:
                        sql_update = "update news.gn_company_keywords set history_flag = 1 where company_code = %s and keyword_type = %s"
                        news_cur.execute(sql_update, (row.company_code, row.keyword_type))
                        news_con.commit()
                        
                    sql_insert = "INSERT INTO news.gn_company_keywords ( company_code, keyword, keyword_type, auto_flag) VALUES (%s, %s, %s, %s)"
                    news_cur.execute(sql_insert, (row.company_code, row.keyword, row.keyword_type, '1'))
                    news_con.commit()
            
            if df_delete.empty == False:
                delete_company_code = df_delete['company_code'].drop_duplicates().to_list()
                for company_code in delete_company_code:
                    sql_update_use_flag = "update news.gn_company_keywords set use_flag = 0 where company_code = %s"
                    news_cur.execute(sql_update_use_flag, (company_code))
                    news_con.commit()
        except Exception as e:
            print(e)
        finally:
            news_cur.close()
            news_con.close


        print(f"Total order value is: {total_order_value:.2f}")






batch_company_synonyms = task_batch_company_synonyms()



```





# DB sync

```py


from airflow.decorators import dag, task
from IPython.display import display

import requests
import pandas as pd
import pymysql
from pymysql.constants import CLIENT
import json
import os
from sqlalchemy import create_engine, delete

from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3
from bs4 import BeautifulSoup

import logging
from pprint import pprint
from datetime import datetime
import time
from pytz import timezone

'''
# dag 반영 
python3 -c "from airflow.models import DagBag; d = DagBag();"
'''

################################################ variables

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

pd.set_option('display.max_columns', None)

################################################ dart crft
# api key : 5e99205e2b9885da9519dd55c253d9a7d70fbab3
# dev api key
# company key : 28528d21a64631809f7665a9c3b0d5e32d0faac5
crtfc_key = '28528d21a64631809f7665a9c3b0d5e32d0faac5'

################################################ mysql 

news_con_str = 'mysql+pymysql://admin:2323!@fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/news'
news_engine = create_engine(news_con_str)
news_con = news_engine.connect()

fngo_con_str = 'mysql+pymysql://fngo:22323@bigfinance-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/fngo'
fngo_engine = create_engine(fngo_con_str)
fngo_con = fngo_engine.connect()


################################################ dags

default_args={
    "owner": "aicel_airflow",
    "depends_on_past": False,
}

@dag(default_args=default_args, schedule_interval='0 9 * * *', start_date=datetime(2021, 1, 1), catchup=False, tags=['pipeline', 'common', 'sync'])
def sync_common_data(multiple_outputs=True):

    @task()
    def task_sync_company():
        target_table = ['company', 'company_filters', 'company_whitelist']

        for table in target_table:   
            print(f'sync table - {table}')             
            df_sync = pd.read_sql('select * from {}'.format(table), con=fngo_con )
            display(df_sync.head(10))
            print(len(df_sync))
            news_engine.execute("DELETE FROM gn_{}".format(table))
            df_sync.to_sql(name='gn_{}'.format(table), con=news_con, if_exists='append', index=False)

        fngo_con.close()
        news_con.close()

        return {'result':1}

    @task()
    def task_get_dart_code(dummy:int):   
        # corp_code 정보 가져 오기 
        local_path = '/home/ubuntu/data/'
        local_file = 'CORPCODE.zip'


        remote_url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={crtfc_key}"
        data = requests.get(remote_url)
        # Save file data to local copy
        with open(local_path + local_file, 'wb')as file:
            file.write(data.content)

        print('start unzip!!')
        
        os.system(f'unzip {local_path + local_file} -d {local_path}' )
        os.system(f'rm {local_path + local_file}' )

        # load corp code data to MySql
        db_connection_str = 'mysql+pymysql://admin:2323!@fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/news'
        db_connection = create_engine(db_connection_str)
        #conn = db_connection.connect()

        # df = pd.DataFrame(columns = ['corp_code', 'corp_name', 'stock_code', 'modify_date'], dtype='object')
        # df = df.astype({'corp_code':'str'})
        df = pd.read_xml(local_path + 'CORPCODE.xml')
        df.to_sql(con=db_connection , name='dart_corp_code', if_exists='replace', index=False)

        return {'result':1}

    res = task_sync_company()
    task_get_dart_code(res)

sync_data = sync_common_data()



```
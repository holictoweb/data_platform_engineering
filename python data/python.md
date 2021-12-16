# time

```python
import datetime 

# 현재 시간 가져 오기 
current = datetime.datetime.now()

# 1시간 후 
one_hour_later = current + datetime.timedelta(hours=1) 

# 1시간 전 
one_hour_ago = current - datetime.timedelta(hours=1)
# 내일 시간 
tomorrow = current + datetime.timedelta(days=1) 
# 어제 시간 
yesterday = current - datetime.timedelta(days=1) 
# 10분 후 
ten_minutes_later = current + datetime.timedelta(minutes=10) 
# 10분 전 
ten_minutes_later = current - datetime.timedelta(minutes=10)



# string to time 
from datetime import datetime

date_time_str = '2021/09/19 01:55:19'
date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
print(date_time_obj)


# timezone now 
from pytz import timezone
current = datetime.datetime.now(timezone('Asia/Seoul')
                                
                                
# 소요 시간 확인 용
start_time = time.perf_counter()

```





# 작업 폴더 변경

```python
import os
# 현재 작업 디렉토리 
os.getcwd()

# 디렉토리 변경
os.chdir('/home/ubuntu')


```



#  logger 사용법

```python
import logging

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

# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


for i in range(10):
	logger.info(f'{i}번째 방문입니다.')
    
```





#  json file load

```python
import pandas as pd
import json

with open('myfile.json') as f:
    jsonstr = json.load(f)

df = pd.io.json.json_normalize(jsonstr)


```





# encoding 확인 

```python
pip install chardet 

import chardet with open("file.txt", "r") as f: 
    file_data = f.readline() 
print(chardet.detect(file_data.encode()))


```





# data file download  to local

```
```



# json line data를 es로 입력

```python
import json
import pandas as pd
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3
from requests_aws4auth import AWS4Auth

import os
from os.path import isfile, join



def init_oss_client():
    host = 'search-aicel-dev-opensearch-243234.ap-northeast-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'ap-northeast-2' # e.g. us-west-1

    service = 'es'
    # credentials = boto3.Session().get_credentials()
    # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    auth = ('aicel', 'ㅈㄷㅈㄷ!')


    oss_client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    return oss_client

def bulk_insert_oss(target_file, oss_client):

    file = open('/home/aicel/app/files/ko_wiki_proc/'+target_file, 'r')

    lines = file.readlines()

    for index, line in enumerate(lines):
        print(index, end=' ')
        data = json.loads(line)
        
        body = []
        for item in (data.get("sentences", "")):
            body.append(item.get("text", ""))
        body_text = '\n'.join(body)

        #print(data['url'] , data['title'], body_text)
        request_body ={
                'title': data['title'],
                'url' : data['url'],
                'body' : body_text
                }

        oss_client.index(index="wiki", doc_type="_doc", body=request_body)

def get_file_list(path):
    files = os.listdir(path)
    return files
    

if __name__ == '__main__':
    
    oss_client = init_oss_client()
    
    path = '/home/aicel/app/files/ko_wiki_proc/'
    files = get_file_list(path)
    count = 1
    for f in files:
        print(f'{count} : {f}')
        bulk_insert_oss(f, oss_client)
        count += 1

    
```


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
current = datetime.datetime.now(timezone('Asia/Seoul'))
                                
                                
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
## logger 코드 예시
```py
def make_logger(name=None):
    #1 logger instance를 만든다.
    logger = logging.getLogger(name)

    #2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)

    #3 formatter 지정
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    #4 handler instance 생성
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(filename="test.log")
    
    #5 handler 별로 다른 level 설정
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    #6 handler 출력 format 지정
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    #7 logger에 handler 추가
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger
```




#  json file load

```python
import pandas as pd
import json

with open('myfile.json') as f:
    jsonstr = json.load(f)

df = pd.io.json.json_normalize(jsonstr)


```

# zipfile 핸들링
```py
import zipfile

local_path = '/home/ubuntu/data/'
local_file = 'CORPCODE.zip'


remote_url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={crtfc_key}"
data = requests.get(remote_url)
# Save file data to local copy
with open(local_path + local_file, 'wb')as file:
    file.write(data.content)

with zipfile.ZipFile(local_path + local_file, 'r') as zip_ref:
    zip_ref.extractall(local_path)

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



# import module
-  
```py
# 하위폴더 폴더는 패키지 명으로 인식 가능 /sub_dir/ccc.py import
from sub_dir import ccc

# 상위 폴더나 다른 폴더의 경우 절대 경로를 참조 하는 코드를 넣어서 진행 가능. 
# 
os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir)))

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from folder3 import ddd
```
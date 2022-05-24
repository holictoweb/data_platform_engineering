# s3 파일 다운로드


```py
import boto3
s3 = boto3.resource('s3')
s3.meta.client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')


# 위의 방법으로는 정상 진행 되지 않음 
# 실제 파일을 다운로드 
import pandas as pd

s3 = boto3.client('s3')

pbucket = 'nlp-entity-linking-train-set'
pkey = 'rsc/alias_page.json'

local_file = '/home/ubuntu/data/wiki/alias_page.json'

with open(local_file, 'wb') as f:
    s3.download_fileobj(pbucket, pkey, f)


# access key & secret key
# object list 가져 오기
import boto3
import pandas as pd
import json

aws_access_key_id = 'ee'
aws_secret_access_key = 'wefqwef+/23'
s3_client = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

bucket = 'data-delivery-news'
delivery_key = 'free-trial/'
read_key = 'free-trial/2012/1/1/20120102.0000.csv' 


objs = s3_client.list_objects(Bucket=bucket, Prefix =delivery_key)
while 'Contents' in objs.keys():
    objs_contents = objs['Contents']
    for i in range(len(objs_contents)):
        filename = objs_contents[i]['Key']
        print(filename)
# 파일 읽기
import io

response = s3_client.get_object(Bucket=bucket,Key=read_key)
file = response["Body"].read()

pd.read_csv(io.BytesIO(file), delimiter=",")
# 파일 삭제
res = s3_client.delete_object(Bucket=bucket,Key=read_key)
print(res)

# 파일 생성 
key = 'free-trial/test.csv' 
s3_client.put_object(Body='test', Bucket=bucket, Key=key)
```

# s3 데이터 로드 
- s3 의 파일을 직접 읽는 방식 
```py
pip install s3fs

import pandas as pd
import boto3
import io

s3_client = boto3.client("s3")

obj = s3_client.get_object(Bucket="nlp-entity-linking-train-set", Key="rsc/company_people.txt")
print (obj)
target_columns = ['stock_code', 'info']
df_people = pd.read_csv(io.BytesIO(obj["Body"].read()), sep='\t', header=None, names=target_columns, dtype={'stock_code':str,'info':str}  )

df_people['info']  = df_people['info'].astype(str).apply(lambda x : x.replace('"', '').replace('[', ' ').replace(']', ' ') )
display(df_people)

```

# s3 특정 object exists check

```py

```

# s3 list 및 버킷에 있는 오브젝트 확인

```py
import boto3
from pprint import pprint 
import pandas as pd

client = boto3.client('s3')
response = client.list_buckets()

# pprint(response)
response = client.list_objects(
    Bucket='nlp-entity-linking-train-set',
    MaxKeys=20,
)

# pprint(response['Contents'])

df = pd.DataFrame(response['Contents'])
display(df[['Key', 'Size', 'LastModified']])

```
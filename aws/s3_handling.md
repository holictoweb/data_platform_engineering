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

```

# s3 데이터 로드 


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
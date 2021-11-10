- elasticsearch 7.x api document

https://elasticsearch-py.readthedocs.io/en/7.x/api.html

# client 생성

```python
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from pprint import pprint

host = 'search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com'
region = 'ap-northeast-2'

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

oss_client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

```

# index 

```python
# index 전체 리스트
oss_client.indices.get_alias("*")

# index 생성 
oss_client.indices.create(index = 'example_index', body = request_body)

# index 상세 조회 
oss_client.indices.get('naver_news')

# index close open 
oss_client.indices.close()
oss_client.indices.open()
```

#  data

```python
# data 건수 확인 
res = oss_client.cat.count('naver_news_2')

# data 복사 
request_body = {
    "source": {
      "index": "naver_news"
    },
    "dest": {
      "index": "naver_news_2"
    }
  }
 
res = oss_client.reindex(request_body)
 

    
```


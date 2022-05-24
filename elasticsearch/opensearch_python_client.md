- elasticsearch 7.x api document

https://elasticsearch-py.readthedocs.io/en/7.x/api.html

- opensearch api document

https://opensearch.org/docs/1.0/clients/python/

# client 생성

```bash
# key를 이용한 로그인 시 필요
pip install boto3
pip install opensearch-py
pip install requests
pip install requests-aws4auth
```



- aws configure를 적용한 경우 

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

- 직접 입력 혹은 ec2의 role을 통해 인증 하는 경우 

```python
from opensearchpy import OpenSearch, RequestsHttpConnection
host = 'search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com' 
region = 'ap-northeast-2'
service = 'es'
auth = ('aicel', 'wefw!')
oss_client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
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

# index 삭제 
oss_client.indices.delete('dart_report_2')

# copy index data 
request_body = {
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter"
  }
}
oss_client.indices.reindex(request_body)
```

# alias

```python
# alias
request_body = {
  "actions": [
    {
      "remove": {
        "index": "dart_report_words",
        "alias": "latest_dart_report"
      }
    },
    {
      "add": {
        "index": "dart_report_words_2",
        "alias": "latest_dart_report"
      }
    }
  ]
}


# alias 를 생성하며 인덱스 전달 
res = oss_client.indices.put_alias(index='company_overview_' + timestamp, name = 'company_overview')
        pprint(res)



```



# index settings update

```python
request = {
  "settings": {
    "similarity": {
      "scripted_tfidf": {
        "type": "scripted",
        "weight_script": {
          "source": "double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;"
        },
        "script": {
          "source": "double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;"
        }
      }
    }
  }
}

res = oss_client.indices.put_settings( index = 'dart_report_search_custom_2', body = request)
pprint(res)
```

```python

oss_client.close(index='dart_report_search_custom', wait_for_active_shards=0)
```

# index mapping update 

```py
put_mapping(body, index=None, doc_type=None, params=None, headers=None)


request_body={
  "properties": {
    "synonyms": {
      "type": "text",  "analyzer": "korean" , "search_analyzer": "korean" 
    }
  }
}
res = oss_client.indices.put_mapping(index = 'wiki_dev', body = request_body)
pprint(res)

```

#  data

```python
# data 건수 확인 
res = oss_client.cat.count('naver_news_2')

    
```

# search

```py
res = oss_client.search(index = 'wiki_dev', body = {"query":{"match":{	"title":"동군연합"}}})
pprint(res['hits']['hits'])



```

# Sort

```python
# match_phrase
request_body = {
    "query": {
        "bool":{
            "must":{
                "match_phrase": {
                    "report":{
                        "query":query_input
                    }
                }
            }
        }
    }
}    


sort_request = '''
"sort":[
            {
                "_score":{"order":"desc"}
            }
        ]
'''

request_source = ["corp_cls", "corp_code", "corp_name",  "rcept_dt", "rcept_no",  "report_nm", "stock_code", "rm" ]
list_report = oss_client.search(index=target_index, doc_type="_doc", _source= request_source,  body = request_body, sort= sort_request,  size = query_count, timeout='20s')
```



# Analyze

```python
text_ana = '''
삼성전자가 전체 주가에 미치는 영향 분석
'''
request_body = {
  "text": text_ana,
  "tokenizer": "seunjeon_tokenizer",
  "filter": [
    "stop",
    "snowball"
  ]
}
res = oss_client.analyze(body = request_body)
```





_ _ _

# explain handling 

```python
# 검색 쿼리 확인 
request_body = {
  "query": {
    "match": {
      "report": "메타버스"
    }
  },
  
}

request_source = ["corp_cls", "corp_code", "corp_name",  "rcept_dt", "rcept_no",  "report_nm", "stock_code", "rm" ]
list_report = oss_client.search(index="dart_report_2", doc_type="_doc", _source= request_source,   body = request_body)
        
pprint(list_report)

# 점수 확인
target_id = 'Uga4_nwBYZczGgQO4Hy7'

res = oss_client.explain(index="dart_report_2", id=target_id,  body=request_body)
pprint(res)

# 검색 결과로 본문 내용 확인 
for doc in list_report['hits']['hits']:
    print(doc['_id'], doc['_source']['report_nm'], doc['_source']['corp_name'])
    res = oss_client.explain(index="dart_report_2", id=doc['_id'],  body=request_body)
    
    res['explanation']


```



_ _ _



## explain 결과 확인 parsing

```python
import requests
import pandas as pd
import pymysql
import json
import os
import time
from sqlalchemy import create_engine
#from xml.etree.ElementTree import parse

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from bs4 import BeautifulSoup

from pprint import pprint


# company key : 28528d21a64631809f7665a9c3b0d5e32d0faac5
crtfc_key = '28528d21a64631809f7665a9c3b0d5e32d0faac5'

local_path = '/home/ubuntu/zeppelin/notebook/src/data/'


########################################################### elastic search
host = 'search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'ap-northeast-2' # e.g. us-west-1

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

# for idx, row in df_crawled.iterrows():
#     #print(row.to_json(force_ascii=False))
#     search.index(index="naver_news", doc_type="_doc", body=row.to_json(force_ascii=False))
########################################################### elastic search

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('mode.chained_assignment',  None)

# Dynamic Forms
query_input = z.textbox("search keyword")
query_count = z.select("query count", [("20","20"), ("50","50"), ("100","100"), ("200","200")] , "20")


target_index = z.select("target_index", [ ("dart_report_search", "dart_report_search")], "dart_report_search")


term_types = ['N', 'SL', 'SH', 'SN']

# 1. 공백 check
if len(query_input.split(' ')) > 1:
    query_input_merge = query_input.replace(" ", "")
    query_input_split = query_input
else:
    query_input_merge = query_input
    
    search_keywords = ''
    analyze_body = {
      "text": query_input,
      "tokenizer": "seunjeon_tokenizer"
    }
    
    analyze_keyword = oss_client.indices.analyze(index=target_index,   body = analyze_body)
    
    for term in analyze_keyword['tokens']:
        if term['type'] in term_types :
            # print(term['token'])
            search_keywords = search_keywords + ' ' + term['token'].split('/')[0] 

    search_keywords = search_keywords.strip()
    query_input_split = search_keywords



# match_phrase
request_body = {
    "query": {
        "bool":{
            "should":{
                "match_phrase": {
                    "report":{
                        "query":query_input_merge
                    }
                },
                "match_phrase": {
                    "report":{
                        "query":query_input_split
                    }
                }
            }
        }
        
    }
}

request_source = ["corp_cls", "corp_code", "corp_name",  "rcept_dt", "rcept_no",  "report_nm", "stock_code", "rm" ]
list_report = oss_client.search(index=target_index, doc_type="_doc", _source= request_source,   body = request_body, size = query_count)
        
#pprint(list_report)

base_colomns = ['id', 'corp_name', 'report_nm', 'rcept_no',  'score', 'hits', 'term', 'boost', 'idf', 'tf' ]
df  = pd.DataFrame(columns = base_colomns)

# 검색 단어의 hit 수 확인 
for doc in list_report['hits']['hits']:
    
    res = oss_client.explain(index=target_index, id=doc['_id'],  body=request_body)
    #pprint(res)
    
    search = res['explanation']
    
    #pprint(search)
        
    while 1:
        #pprint(search['description'])
        if isinstance(search, list):
            # print('search is list')
            if str(search[0]['description'])[:6] == 'weight':
                break
        else:
            if str(search['description'])[:6] == 'weight':
                break
        
        search = search['details']
    
    # pprint(search)
    
    if isinstance(search, list): 
        for search_row in search:
            # print('search_row!')
            
            term = search_row['description'].split(':')[1].split(" ")[0]
            boost = search_row['details'][0]['details'][0]['value']
            idf = search_row['details'][0]['details'][1]['value']
            tf = search_row['details'][0]['details'][2]['value']
            hits = search_row['details'][0]['details'][2]['details'][0]['value']
        
            df_idx = len(df)
            df.loc[df_idx] = [doc['_id'], doc['_source']['corp_name'], doc['_source']['report_nm'], doc['_source']['rcept_no'],  doc['_score'],  hits, term, boost, idf, tf]
    else:
        
        # if len(query_input.strip().split(" ")) > 1:
        #     term = search['description'].split('"')[1]
        # else:
        
        term = search['description']
        if len(query_input_split.split(' ')) > 1:
            term = search['description'].split(':')[1].split("\"")[1]  
        else:
            term = search['description'].split(':')[1].split(" ")[0]
        boost = search['details'][0]['details'][0]['value']
        idf = search['details'][0]['details'][1]['value']
        tf = search['details'][0]['details'][2]['value']
        hits = search['details'][0]['details'][2]['details'][0]['value']
        
        df_idx = len(df)
        df.loc[df_idx] = [doc['_id'], doc['_source']['corp_name'], doc['_source']['report_nm'], doc['_source']['rcept_no'],  doc['_score'],  hits, term, boost, idf, tf]
        
    
    # break

    
# display(df)
df.hits = df.hits.astype("float")
df.score = df.score.astype("float")
df.sort_values(by="hits", ascending = False, inplace = True)
z.show(df)
# display(df)

```






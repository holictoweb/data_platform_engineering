



# 1. 검색 angular



```python


angular_header = '''
%angular

<script>

function appendSerch(checkbox_id) {
    check_box = document.getElementById(checkbox_id)
    if(check_box.checked) 
    {
        append_keyword = checkbox_id
        var elem = document.getElementById('search_keyword');
        elem.value += ' ' + append_keyword;
    }
    $( "#search_keyword" ).change();
}

function changemodel(){
    alert('test change');
}

var scope = angular.element("#test").scope();


</script>
 
<body ng-app="demo" ng-controller="DemoController">

<div class="row">
    <div class="col-md-4">
        <form class="form-inline">
            <label>Find Synonym : </label>
            <input type="text" id="keyword" ng-model="inputText"></input>
            <button type="submit" class="btn btn-primary" ng-click="z.runParagraph('paragraph_1638344751784_533930122'); z.angularBind('input_text', inputText, 'paragraph_1638344751784_533930122')">Find</button>
            <button type="submit" class="btn btn-info" ng-click="z.runParagraph('paragraph_1638344751784_533930122'); z.angularBind('input_text', 'reset', 'paragraph_1638344751784_533930122')">Reset</button>
        </form>
    </div>
    <div class="col-md-8">
    </div>
</div>
<hr>
'''

angular_check = '' #초기화
for idx in range(len(keyword_list)):
    checkbox_id = 'check_'+str(idx)
    angular_check = angular_check + f'''
    <div class="form-check form-check-inline col-md-2">
        <input class="form-check-input" type="checkbox" value="" id="{keyword_list[idx]}" onclick="appendSerch('{keyword_list[idx]}')">
        <label class="form-check-label" for="{keyword_list[idx]}">
        {keyword_list[idx]}
        </label>
    </div>
    '''
angular_synonym = '<div class="row">' + angular_check + '</div>' 

angular_footer ='''
<hr>
<div class="row>
    <div class="col-md-9">
        <form class="form-inline">
            <label class="col-lg-1">Elasticsearch</label>
            <input type="text" class="col-lg-7" id="search_keyword" ng-model="searchText"></input>
            &nbsp
            <select id="query_type" class="form-select" aria-label="Default example" ng-model="searchType">
              <option value="must" selected>and</option>
              <option value="should">or</option>
            </select>
            <button type="submit" class="btn btn-primary" ng-click="z.runParagraph('paragraph_1638238203238_507308036'); z.angularBind('query_input', searchText , 'paragraph_1638238203238_507308036'); z.angularBind('query_type', searchType , 'paragraph_1638238203238_507308036')"> Search</button>
            <!--<button type="submit" class="btn btn-primary" ng-click="z.runParagraph('paragraph_1638344751784_533930122')"> Reset</button>-->
        </form>
    </div>
</div>
<hr>

</body>
'''

print(angular_header + angular_synonym + angular_footer)



```

# 2. es 실제 검색

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
import re

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
# query_input = z.textbox("search keyword")
# query_type = z.select("search type", [('should', 'or'), ('must', 'and')], 'and')
# query_count = z.select("query count", [("20","20"), ("50","50"), ("100","100"), ("200","200"), ("400","400"), ("1000","1000")] , "20")


query_input = z.z.angular("query_input")
query_type = z.z.angular("query_type")
print(query_input)
print(query_type)

query_type = 'must'

target_index = z.select("target_index", [("dart_report_search", "dart_report_search"), ("dart_report_search_all", "dart_report_search_all")], "dart_report_search")
# target_index = 'dart_report_search_all'

term_types = ['N', 'SL', 'SH', 'SN']

operation_type = 'or'
keyword_list = []
request_keyword = ''

query_input_list = query_input.split(' ')
if len(query_input_list) > 1:
    for idx in range(len(query_input_list)):
        # print(idx)
        keyword = query_input_list[idx]
        
        # print(keyword)
        if idx != 0:
            request_keyword = request_keyword + ','
        
        request_keyword = request_keyword + "{'match_phrase':{'report':{'query':'" + keyword + "'}}}"
        
    request_body = "{'query':{'bool':{'" + query_type + "':[" + request_keyword + "]}}}"
    
    request_body = eval(request_body)
    pprint(request_body)
    
else : 
        
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
            
#     request_keyword = "{'should':{" + request_keyword + "}}"

# pprint(request_keyword)
# request_keyword = ast.literal_eval(request_keyword)

# pprint(request_keyword)




request_source = ["corp_cls", "corp_code", "corp_name",  "rcept_dt", "rcept_no",  "report_nm", "stock_code", "rm" ]
list_report = oss_client.search(index=target_index, doc_type="_doc", _source= request_source,   body = request_body, size = 1000, timeout='20s')


base_colomns = ['rcept_no', 'corp_name', 'report_nm', 'term', 'score', 'hits', 'idf', 'tf',  'boost' ]
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
            term = search_row['description']
            term = re.findall(r'report:(.+?)[,\]]',term)
            boost = search_row['details'][0]['details'][0]['value']
            idf = search_row['details'][0]['details'][1]['value']
            tf = search_row['details'][0]['details'][2]['value']
            hits = search_row['details'][0]['details'][2]['details'][0]['value']
        
            df_idx = len(df)
            df.loc[df_idx] = [doc['_source']['rcept_no'], doc['_source']['corp_name'], doc['_source']['report_nm'], term, doc['_score'],  hits, idf, tf, boost]
    else:
        
        # if len(query_input.strip().split(" ")) > 1:
        #     term = search['description'].split('"')[1]
        # else:
        
        term = search['description']
        
        term = re.findall(r'report:(.+?)[,\]]',term)
        # if len(query_input_split.split(' ')) > 1:
        #     term = search['description'].split(':')[1].split("\"")[1]  
        # else:
        #     term = search['description'].split(':')[1].split(" ")[0]
        boost = search['details'][0]['details'][0]['value']
        idf = search['details'][0]['details'][1]['value']
        tf = search['details'][0]['details'][2]['value']
        hits = search['details'][0]['details'][2]['details'][0]['value']
        
        df_idx = len(df)
        df.loc[df_idx] = [doc['_source']['rcept_no'], doc['_source']['corp_name'], doc['_source']['report_nm'], term, doc['_score'],  hits, idf, tf, boost]
        
    
    # break

    
# display(df)
df.hits = df.hits.astype("float")
df.score = df.score.astype("float")
df.sort_values(by="hits", ascending = False, inplace = True)
z.show(df)
# display(df)

```


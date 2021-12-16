- es document

- https://esbook.kimjmin.net/

# DATA CRUD

## create

```bash
# index 생성
PUT /dev

```



- crete uesr

```json
PUT _plugins/_security/api/internalusers/aicel02
{
  "password": "Aicel2021!",
  "opendistro_security_roles": ["maintenance_staff", "weapons"],
  "backend_roles": ["captains", "starfleet"],
  "attributes": {
    "attribute1": "value1",
    "attribute2": "value2"
  }
}
```



## insert

-  bulk insert 

```bash
curl -XPOST 'localhost:9200/bank/account/_bulk?pretty&refresh' -H "Content-Type: application/json" --data-binary "@test_data.json"
```

## delete

```bash
# index 삭제
DELETE /sample-index

# index data 만 삭제 (?)

```



## 조회

```bash

curl -XPUT 'localhost:9200/member?pretty'

# index 리스트 조회 
GET _aliases

# index 정보 조회
GET /{index_name}

# 인덱스로 부터 데이터 조회
GET my_index/_doc/1
```



# 검색 관련



- full text  검색과 관련된 유형
- https://esbook.kimjmin.net/05-search/5.1-query-dsl

```
match_all, match, match_phrase, query_string
```



## 1. analyze 결과 확인

```json
GET _analyze
{
  "text": "삼성전자가 전체 주가에 미치는 영향 분석",
  "tokenizer": "seunjeon_tokenizer",
  "filter": [
    "stop",
    "snowball"
  ]
}
```



## 2. 검색

- query string query 를 통해 조회

- ## match

    match 쿼리는 풀 텍스트 검색에 사용되는 가장 일반적인 쿼리입니다. 다음은 match 쿼리를 이용하여 my_index 인덱스의 message 필드에 **dog** 가 포함되어 있는 모든 문서를 검색합니다.

  여러 개의 검색어를 집어넣게 되면 디폴트로 **OR** 조건으로 검색이 되어 입력된 검색어 별로 하나라도 포함된 모든 문서를 모두 검색합니다.

```json
GET dart_report/_search/
{
  "query": {
    "match": {
      "report": "메타버스"
    }
  }
}

# 하나의 쿼리에서 조건 유형
GET dart_report/_search
{
  "size" : 3,
  "query": {
    "match": {
        "report":{
            "query":"삼성전자 LG전자",
            "operator":"and"       
        }
    }
  },
  "_source": "corp_name"
  
}


# 여러 필드 검색 
GET dart_report/_search/
{
  "query": {
    "multi_match": {
        "query":q,
        "operator":"and",
        "fields":[
            "report_nm^4",
            "report"
            ]
    }
  },
}

# sort

{
    "sort"{
        {"rate":"desc"},
        "_score"
    },
    "query":{
        "match_all":{}
    }
}


```

- multi match 
- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html

```json
# multi match 
GET /_search
{
  "query": {
    "multi_match" : {
      "query":    "this is a test", 
      "fields": [ "subject", "message" ] 
    }
  }
}

# boosting
GET /_search
{
  "query": {
    "multi_match" : {
      "query" : "this is a test",
      "fields" : [ "subject^3", "message" ] 
    }
  }
}



```



## 2. 유사도 결과 확인

- 검색 내용까지 포함해야 함. 

```json
GET /my-index-000001/_explain/{id}
{
  "query" : {
    "match" : { "message" : "elasticsearch" }
  }
}
```



# 3. index setting 변경



## 4. 쿼리 변경 

```json
POST /_sql/translate
{
  "query": "SELECT * FROM library ORDER BY page_count DESC",
  "fetch_size": 10
}
```


# create

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



# 조회

```bash

curl -XPUT 'localhost:9200/member?pretty'

# index 리스트 조회 
GET _aliases

# index 정보 조회
GET /{index_name}

# 인덱스로 부터 데이터 조회
GET my_index/_doc/1
```



# delete

```bash
# index 삭제
DELETE /sample-index

# index data 만 삭제 (?)

```



_ _ _



# DATA CRUD



```



```





_ _ _

# 검색 관련



## 1. anlayze 결과 확인

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

```json
GET dart_report/_search/
{
  "query": {
    "match": {
      "report": "메타버스"
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


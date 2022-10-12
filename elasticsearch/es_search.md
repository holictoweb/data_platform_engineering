

# search

## 기본 쿼리
```py
# 전체 조회 
res = oss_client.search(index="naver_news")
pprint(res)

```
### sort
```py
res = oss_client.search(index='naver_news', sort='published_at:desc')
pprint(res)
```
### select columns
```py

```

```json
# 가중치 부여 쿼리 
{
    "query": {
        "function_score": {
            "query": { "match": { "itemname": "아이폰 케이스" } },
            "boost": "5",
            "functions": [
                {
                    "filter": { "match": { "viewKeywords": "아이폰 케이스" } },
                    "random_score": {},
                    "weight": 23
                },
                {
                    "filter": { "match": { "buyKeywords": "아이폰 케이스" } },
                    "weight": 42
                }
            ],
            "max_boost": 42,
            "score_mode": "max",
            "boost_mode": "multiply",
            "min_score" : 0
        }
    }
}'

```







### 1.  단순 검색 

```bash
# term 단순 조회 
{
	"query":{
		"match":{
			"field":"value"
		}
	}
}
```





### 2. 구문 전체가 일치 

```bash
{
  "query": {
    "match_phrase": {
      "title": "Awesome elasticsearch"
    }
  }
}
```



### 3. 여러 필드 search

```bash
{
  "query": {
    "multi_match": {
      "title": "Awesome Elastic",
      "fields": ["title", "contents"]
    }
  }
}
```



### 4. bool사용

```bash
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": {
              "query": "lazy dog"
            }
          }
        }
      ],
      "should": [
        {
          "match_phrase": {
            "message": "lazy dog"
          }
        }
      ]
    }
  }
}

{'query': {'bool': {'must': [{'match_phrase': {'report': {'query': '분기보고서'}}},
                             {'match_phrase': {'report': {'query': '삼성전자'}}}]}}}
                             
```



### highlight

```json
{
    "query": {
        "bool":{
            ...
        }
    },
    "highlight" : {
        "pre_tags": ["<b style='font-size:1.2em'>"],
        "post_tags": ["</b>"],
        "fields" : {
            "report" :  {"fragment_size" : 200, "number_of_fragments" : 200}
        }
    }
}
    


{
  "query": {
    "match": { "content": "kimchy" }
  },
  "highlight": {
    "fields": {
      "content": {}
    }
  }
}

```





# Search Template

- https://www.elastic.co/guide/en/elasticsearch/reference/7.7/search-template.html







```PYTHON
POST _scripts/demo_search_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "content": {
                  "query": "{{query_string}}"
                }
              }
            },
            {
              "match": {
                "content": {
                  "query": "{{query_string}}",
                  "operator": "and"
                }
              }
            },
            {
              "match_phrase": {
                "content": {
                  "query": "{{query_string}}",
                  "boost": 2
                }
              }
            }
          ]
        }
      }
    }
  }
}


# 선언한 tamplate 사용
GET _search/template
{
    "id": "demo_search_template", 
    "params": {
        "query_string": "simple rest apis distributed nature"
    }
}


```




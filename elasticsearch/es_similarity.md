- 

https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html#_available_similarities

# 기본 로직 적용 
- BM25, tf/idf(classic)
- https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html

```python
# BM25
검색 대상 키워드들의 결과 값을 모두 합산 
idf = log(1 + (N -n + 0.5) / (n + 0.5) ) 
n = number of documnets containing term
N = total number of documents with field

키워드 전체 히트를 기반으로 산정 ( 개발 키워드 합산은 아님 )
tf = freq / (freq + k1 * (1- b + b * dl /avgdl))
k1 = term saturation parameter ( default 1.2)
b = length normalization paramter ( default 0.75 )
dl = length of field (approximate)
avgdl = average length of field


```

1. simirality 를 적용 하더라도 simirality 를 mapping 하기 위한 작업이 re-index 가 필요 
2. 


## DFR 적용
```py
reqest_body = {
  "settings": {
    "index": {
      "similarity": {
        "my_similarity": {
          "type": "DFR",
          "basic_model": "g",
          "after_effect": "l",
          "normalization": "h2",
          "normalization.h2.c": "3.0"
        }
      }
    }
  }
}

res = oss_client.indices.put_settings(index='dart_report_search_custom', body = reqest_body)
```




# 기존 index에 script simirality 적용
```py
request = {
    "settings":{
        "similarity": {
            "scripted_tfidf_2": {
                "type": "scripted",
                "script": {
                    "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                }
            }
        }    
    }
    
}

res = oss_client.indices.put_settings( index = 'dart_report_search_custom', body = request)
pprint(res)
```


# index filed 에 simirality mapping 적용 
```python
request = {
    "properties":{
        "report_path": {'analyzer': 'korean',
            'similarity': 'my_similarity',
            'type': 'text'
            }
    }
}

res = oss_client.indices.put_mapping( index = 'dart_report_search_custom', body = request)
pprint(res)
```


# index 적용 



```python
# similarity 인덱스 재 생성 
request_body = {
    "mappings": {"properties": {"Unnamed: 0": {"type": "long"
            },
      "corp_cls": {"type": "text",
       "fields": {"keyword": {"type": "keyword", "ignore_above": 256
                    }
                }
            },
      "corp_code": {"type": "long"
            },
      "corp_name": {"type": "text",
       "fields": {"keyword": {"type": "keyword", "ignore_above": 256
                    }
                }
            },
      "flr_nm": {"type": "text",
       "fields": {"keyword": {"type": "keyword", "ignore_above": 256
                    }
                }
            },
      "rcept_dt": {"type": "long"
            },
      "rcept_no": {"type": "long"
            },
      "report": {"type": "text", "analyzer": "korean" , "search_analyzer": "korean", "similarity":"scripted_tfidf"},
      "report_nm": {"type": "text",
        "fields": {"keyword": {"type": "keyword", "ignore_above": 256
                    }
                }
            },
      "rm": {"type": "text",
       "fields": {"keyword": {"type": "keyword", "ignore_above": 256
                    }
                }
            },
      "stock_code": {"type": "long"
            }
        }
    },
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "korean": {
                        "type": "custom",
                        "tokenizer": "seunjeon"
                    }
                },
                "tokenizer": {
                    "seunjeon": {
                        "user_words": [],
                        "index_eojeol": "true",
                        "user_dict_path": "analyzers/F224585812",
                        "index_poses": [
                            "UNK",
                            "EP",
                            "I",
                            "J",
                            "M",
                            "N",
                            "SL",
                            "SH",
                            "SN",
                            "VCP",
                            "XP",
                            "XS",
                            "XR"
                        ],
                        "decompound": "true",
                        "type": "seunjeon_tokenizer"
                    }
                }
            }
        },
        "similarity": {
            "scripted_tfidf": {
                "type": "scripted",
                "script": {
                    "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                }
            }
        }
    }
}



oss_client.indices.create(index = 'dart_report_search_custom', body = request_body)

```



# 적용 원복

```json
POST /index/_close?wait_for_active_shards=0

PUT /index/_settings
{
  "index": {
    "similarity": {
      "default": {
        "type": "boolean"
      }
    }
  }
}

POST /index/_open

```


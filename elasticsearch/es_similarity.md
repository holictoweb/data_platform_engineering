- 

https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html#_available_similarities

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


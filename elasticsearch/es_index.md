

# opensearch



|es|db|
|--------------------|--------------|
| field            | column |
| document         | row    |
| index            | table  |
| type(deprecated) | table  |
| mapping          | schema |
| _id              | pk     |



# 문자열 text, keyword



- `"analyzer" : "<애널라이저명>"` - 색인에 사용할 애널라이저를 입력하며 디폴트로는 standard 애널라이저를 사용합니다. 토크나이저, 토큰필터들을 따로 지정할수가 없으며 필요하다면 사용자 정의 애널라이저를 settings에 정의 해 두고 사용합니다.

- `"search_analyzer" : "<애널라이저명>"` - 기본적으로 text 필드는 match 쿼리로 검색을 할 때 색인에 사용한 동일한 애널라이저로 검색 쿼리를 분석합니다. **search_analyzer** 를 지정하면 검색시에는 색인에 사용한 애널라이저가 아닌 다른 애널라이저를 사용합니다. 보통 **NGram** 방식으로 색인을 했을 때는 지정 해 주는 것이 바람직합니다.

- `"index" : <true | false>` - 디폴트는 **true** 입니다. false로 설정하면 해당 필드는 역 색인을 만들지 않아 검색이 불가능하게 됩니다.

- `"boost" : <숫자 값>` - 디폴트는 1 입니다. 값이 1 보다 높으면 풀텍스트 검색 시 해당 필드 스코어 점수에 가중치를 부여합니다. 1보다 낮은 값을 입력하면 가중치가 내려갑니다.

- `"fielddata" : <true | false>` - 디폴트는 false 입니다. true로 설정하면 해당 필드의 색인된 텀 들을 가지고 **집계(aggregation)** 또는 **정렬(sorting)**이 가능합니다. 이 설정은 다이나믹 설정으로 이미 정의된 매핑에 true 또는 false로 다시 적용하는 것이 가능합니다.





# opensarch 은전한닢 index 설정

- https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-plugins.html

- [aws document Amazon Elasticsearch Service, 한국어 분석을 위한 ‘은전한닢’ 플러그인 지원](https://aws.amazon.com/ko/blogs/korea/amazon-elasticsearch-service-now-supports-korean-language-plugin/)



## sysnonym user-dict 설정

```python
# 인덱스 재 생성 
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
      "report": {"type": "text", "analyzer": "korean" , "search_analyzer": "korean"},
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
                        "tokenizer": "seunjeon",
                        "filter": ["dart_filter"]
                    }
                },
                "tokenizer": {
                    "seunjeon": {
                        "user_words": [],
                        "user_dict_path": "analyzers/F147440239",
                        "index_eojeol": "true",
                        "index_poses": [
                            "N", "SL", "SH", "SN"
                        ],
                        "decompound": "false",
                        "type": "seunjeon_tokenizer"
                    }
                },
                "filter":{
                    "dart_filter":{
                        "type": "synonym",
                        "synonyms_path": "analyzers/F221957889"
                    }
                }
            }
        }
    }
}



oss_client.indices.create(index = 'dart_report_prod_2', body = request_body)

```











```json
# 은전한닙 활성화
curl -XPOST 'https://search-korean-text-xxxxx.ap-northeast-2.es.amazonaws.com/mytext/' -d ' {
    "index":{
        "analysis":{
            "tokenizer" : {
                "seunjeon" : {
                    "type" : "seunjeon_tokenizer"
                }
            },
            "analyzer" : {
                "analyzer" : {
                    "type" : "custom",
                    "tokenizer" : "seunjeon"
                }
            }
        }
    }
}'






```



- user_dict, synonyms 설정 적용

```python
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
                        "user_dict_path": "analyzers/F147440239",
                        "index_eojeol": "true",
                        "index_poses": [
                            "N"
                        ],
                        "decompound": "false",
                        "type": "seunjeon_tokenizer",
                        "filter": ["dart_synonym"]
                    }
                },
                "filter":{
                    "dart_synonym":{
                        "type": "synonym",
                        "synonyms_path": "analyzers/F221957889",
                        "updateable": "true"
                    }
                }
            }
        }
    }
```



- analyzer 테스트

```bash
# index 생성 및 analyzer 설정 
PUT /dart_dev_words
{
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
                        "user_words": ["삼성전자", "골구", "맥퀸"],
                        "index_eojeol": "true",
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
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "korean"
            },
            "body": {
                "type": "text",
                "analyzer": "korean"
            }
                        },
            "body": {
                "type": "text",
                "analyzer": "korean"
            }        
        }
    }
}

# setting 변경  ( X ) 
# 실행 하기 위해선 해당 index 를 먼저 close 하고 수행 해야함. 
# mapping의 경우 기존 할당된 정보를 변경하는것이 불가 하며 결국 index 를 새로 생성하고 데이터를 옮기는 작업을 진행해야 함. 
PUT /dart_dev/_settings
{
  "index" : {
    "analysis" : {
    	"tokenizer":{
    		"seunjeon":{
    			"user_words": ["삼성전자", "LG전자", "맥퀸"]
    		}
    	}
    }
  }
}

# close open index
POST /dart_dev/_close 
POST /dart_dev/_open

# index data 이관
POST _reindex
{
	"source":{
		"index":"dart_dev"
	},
	"dest":{
		"index":"dart_dev_words"
	}
}


# 데이터 조회 
GET /dart_dev/_analyze
{
	"analyzer":"korean",
	"text":"삼성전자가 결국 갤럭시사업을 포기하였습니다"
}

```







# 스코어링

https://velog.io/@diane_at_work/Elasticsearch-%EA%B8%B0%EB%B3%B8-score-%EA%B3%84%EC%82%B0-%EB%B0%A9%EB%B2%95

- **문서에 해당 키워드가 등장하는 빈도가 작을수록, IDF가 커지면서 score도 올라간다.**
- **검색된 문서에 매칭된 키워드수가 자주 반복될수록, 또 평균 필드 길이보다 검색된 문서의 필드가 길수록 score가 올라간다**.



- ES 공식 문서 (정확도 Relevancy)

https://esbook.kimjmin.net/05-search/5.3-relevancy

# 유사도 모듈

참고 블로그 - https://teahyuk.github.io/services/2019/07/25/elastic-search-scoring-analyzing.html



- https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html

### scoring

- 유사도 모듈의 설정에 따라 각 검색 시 마다 _score로 유사도를 판단하여 검색 함

### [How Shards Affect Relevance Scoring in Elasticsearch](https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch)

- 스코어 계산은 default 로 샤드 기준으로 계산을 함
- 샤드에 document가 어떤 분포로 들어가느냐에 따라 score가 다르게 나올 수 있음



# 벡터 필드를 이용한 텍스트 유사도 검색 

https://www.elastic.co/kr/blog/text-similarity-search-with-vectors-in-elasticsearch





# 인덱스 생성 ( nori ) 

### nori 데이터 테스트

- https://velog.io/@yaincoding/%ED%95%9C%EA%B8%80-%EB%B6%84%EC%84%9D%EA%B8%B0-Nori%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EC%9C%84%ED%82%A4-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%83%89%EC%9D%B8%ED%95%98%EA%B3%A0-%EA%B2%80%EC%83%89-%EC%8B%A4%EC%8A%B5%ED%95%98%EA%B8%B0

- nori 설치 

```bash
# 직접 설치 
./elasticsearch/bin/elasticsearch-plugin install analysis-nori

# docker file 에 지정 
RUN elasticsearch-plugin install analysis-nori
```





```json
PUT /wiki
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "tokenizer": {
        "nori_none": {
          "type": "nori_tokenizer",
          "decompound_mode": "none"
        },
        "nori_mixed": {
          "type": "nori_tokenizer",
          "decompound_mode": "mixed"
        },
        "nori_discard": {
          "type": "nori_tokenizer",
          "decompound_mode": "discard"
        }
      },
      "analyzer": {
        "nori_none": {
          "type": "custom",
          "tokenizer": "nori_none",
          "filter": ["lowercase", "nori_readingform"]
        },
        "nori_mixed": {
          "type": "custom",
          "tokenizer": "nori_mixed",
          "filter": ["lowercase", "nori_readingform"]
        },
        "nori_discard": {
          "type": "custom",
          "tokenizer": "nori_discard",
          "filter": ["lowercase", "nori_readingform"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "nori_mixed"
      },
      "body": {
        "type": "text",
        "analyzer": "nori_mixed"
      }
    }
  }
}
```



- index에 analyzer 를 지정 한 후 해당 analyzer 를 통해 데이터 확인 

```bash
# 한글 분석기 테스트 
POST /wiki/_analyze
{
  "analyzer": "nori_mixed", 
  "text": "수학에서 상수란 그 값이 변하지 않는 불변량으로, 변수의 반대말이다. 물리 상수와는 달리, 수학 상수는 물리적 측정과는 상관없이 정의된다."
}

```








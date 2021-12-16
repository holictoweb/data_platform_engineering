

# 엽전한닙 config



- 기본 파라미터 

| 파라미터       | 설명                                                         |
| -------------- | ------------------------------------------------------------ |
| user_wods      | 사용자 사진을 정의한다(기본값 : [ ])                         |
| user_dict_path | 사용자 사전 파일의 경로를 설정한다. 해당 파일은 엘라스틱서치의 config폴더 밑에 생성한다. |
| decompoud      | 복합명사 분해 여부를 정의한다(기본값 : true)                 |
| deinflect      | 활용어의 원형을 추출한다(기본값 : true)                      |
| index_eojeol   | 어절을 추출한다(기본값 : true)                               |
| index_poses    | 추출할 품사를 정의한다. 품사의 정의는 아래 표 참고 (예 : "N", "SL" ...) |
| pos_tagging    | 품사 태깅 여부를 정의한다(키워드에 품사가 붙어나온다) 기본값은 true |
| max_unk_length | Unknown 품사 태깅의 키워드로 뽑을 수 있는 최대 길이를 정의한다(기본값 : 8) |

 

- 품사 태그

| 품사 태그명 | 설명            |
| ----------- | --------------- |
| UNK         | 알 수 없는 단어 |
| EP          | 선어말어미      |
| E           | 어미            |
| I           | 독립언          |
| J           | 관계언/조사     |
| M           | 수식언          |
| N           | 체언            |
| S           | 부호            |
| SL          | 외국어          |
| SH          | 한자            |
| SN          | 숫자            |
| V           | 용언            |
| VCP         | 긍정지정사      |
| XP          | 접두사          |
| XS          | 접미사          |
| XR          | 어근            |

 





# 사용자 정의 패키지 적용 

- sysnonyms_path, stopwords_path 등을 s3 기반으로 등록 하여 해당 패스의 id 기반으로 settings 에 추가 

https://docs.aws.amazon.com/opensearch-service/latest/developerguide/custom-packages.html



1. Amazon OpenSearch Service 콘솔에서 **패키지 를** 선택합니다 .
2. **패키지 가져오기를** 선택 **합니다** .
3. 패키지에 설명적인 이름을 지정합니다.
4. 파일에 대한 S3 경로를 제공하고 **제출** 을 선택합니다 .
5. **패키지** 화면으로 돌아갑니다 .
6. 패키지 상태가 **사용 가능 인** 경우 선택합니다. 그런 다음 **도메인에 연결을** 선택 **합니다** .
7. 도메인을 선택한 다음 **연결** 을 선택합니다 .
8. 탐색 창에서 도메인을 선택하고 **패키지** 탭으로 이동합니다 .
9. 패키지 상태가 **사용 가능** 이면 해당 ID를 기록해 둡니다. 사용 의 파일 경로로 [오픈 서치 요청](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/custom-packages.html#custom-packages-using) . `analyzers/id`



#  filter 적용

- opensearch 일반적인 sysnonym 적용 방법 
- https://docs.aws.amazon.com/opensearch-service/latest/developerguide/custom-packages.html



- 실제 적용시 정상적으로 적용 되지 않음. 

```python
"settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "korean": {
                        "type": "custom",
                        "tokenizer": "seunjeon",
                        "filter": ["dart_synonym"]
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
                        "type": "seunjeon_tokenizer"

                    }
                },
                "filter":{
                    "dart_synonym":{
                        "type": "synonym",
                        "synonyms_path": "analyzers/F221957889",
                        "updateable": "true" # 자동 update는 인덱스 시점에는 적용 할 수 없으며 search 시점에 적용 
                    }
                }
            }
        }
    }
```


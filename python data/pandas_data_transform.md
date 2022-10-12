



# source

## elasticsearch 
- elasticsearch 수집 데이터 to pandas
```py
from pprint import pprint 
import json 

df_result = pd.DataFrame()

for keyword in keyword_list:
    print(keyword)
    request_body = {
        "query":
        {
            "bool":{
                "should":[
                    {"match":{"title":keyword}},
                    {"match":{"summary":keyword}},
                    {"match":{"body":keyword}}
                ]
            }
        }
    }
    
    res = oss_client.search(index='naver_news', body = request_body)
    # pprint(res)
    print(len(res['hits']['hits']))
    if len(res['hits']['hits']) > 0 :
        df_append = pd.concat(map(pd.DataFrame.from_dict, res['hits']['hits']), axis=1)['_source'].T.reset_index(drop=True)
        df_result = pd.concat([df_result, df_append], ignore_index=True)
    
    
    # display(df_result.tail(1))

print(len(df_result))
display(df_result.head(10))
```
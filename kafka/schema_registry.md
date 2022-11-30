# github
- https://github.com/awslabs/aws-glue-schema-registry


# apache kafka connect 와 연결
- https://docs.aws.amazon.com/ko_kr/glue/latest/dg/schema-registry-integrations.html
![](https://docs.aws.amazon.com/ko_kr/glue/latest/dg/images/schema_reg_int_kafka_connect.png){: width="200" height="100"}


```bash
# github 에서 다운로드 후 

git clone git@github.com:awslabs/aws-glue-schema-registry.git
cd aws-glue-schema-registry
mvn clean install
mvn dependency:copy-dependencies


# msk connect custom plugin 포함 시킬 zip 파일의 lib 에 해당 jar 복사 
/avro-kafkaconnect-converter/target/schema-registry-kafkaconnect-converter-$GSR_LIB_VERSION.jar:
/common/target/schema-registry-common-$GSR_LIB_VERSION.jar
/avro-serializer-deserializer/target/schema-registry-serde-$GSR_LIB_VERSION.jar'

# 복사 한 결과 
(base) ubuntu@ip-10-0-2-115:~/download/confluentinc-kafka-connect-jdbc-10.5.0/lib$ ls
checker-qual-3.5.0.jar                                      osdt_cert-19.7.0.0.jar
common-utils-6.0.0.jar                                      osdt_core-19.7.0.0.jar
jtds-1.3.1.jar                                              postgresql-42.3.3.jar
kafka-connect-jdbc-10.5.0.jar                               schema-registry-common-1.1.12.jar
mssql-jdbc-8.4.1.jre8.jar                                   schema-registry-kafkaconnect-converter-1.1.12.jar
mysql-connector-java-8.0.11.jar                             schema-registry-serde-1.1.12.jar
ojdbc8-19.7.0.0.jar                                         simplefan-19.7.0.0.jar
ojdbc8-production-19.7.0.0.pom                              slf4j-api-1.7.30.jar
ons-19.7.0.0.jar                                            sqlite-jdbc-3.25.2.jar
oraclepki-19.7.0.0.jar                                      ucp-19.7.0.0.jar
orai18n-19.7.0.0.jar                                        xdb-19.7.0.0.jar
original-schema-registry-kafkaconnect-converter-1.1.12.jar  xmlparserv2-19.7.0.0.jar

```
## 스키마 등록 이후 스키마 버젼 조회 확인

```bash
aws glue list-registries --region us-west-2

aws glue get-schema-version --schema-id "RegistryName=news.naver,SchemaName=gn_news_company_table" --schema-version-number "VersionNumber=1"

```

# avro 기본 

## 장단점 
- 장점 
  - 데이터의 타입 확인 가능
  - 압축 
  - 스키마에 설명을 포함하여 구조를 이해하는데 도움을 줄 수 있다
  - shcmema evolution
  - schema registry 를 사용 할 수 있음. 

- data type
  - null 
  - boolean
  - int
  - long
  - float 
  - double
  - bytes
  - string


### 스키마 호환성 모드 
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbSXeAE%2FbtqDIobE5p4%2F41zIKdECX5K1QKOz77Hjo0%2Fimg.png)
- Backward :
    컨슈머는 2번 스키마로 메시지를 처리하지만 1번 스키마도 처리할 수 있습니다
    필드 삭제 혹은 기본 값이 있는 필드 추가인 경우

- Forward :  
    컨슈머는 1번 스키마로 메시지를 처리하지만 2번 스키마도 처리할 수 있습니다.
    필드 추가 혹은 기본 값이 있는 필드 삭제
- Full : 
    Backward와 Forward를 모두 가집니다.
    기본 값이 있는 필드를 추가 혹은 삭제
- None :
    스키마 호환성을 체크하지 않습니다.


```avro


{
    "type":"record"

}

```

# avro 스키마 예시 

``` json
{
    "type": "record",
    "namespace": "news.naver",
    "name": "gn_naver_company_table",
    "fields": [
        {
            "name": "news_url_md5",
            "type": "string"
        },
        {
            "name": "company_code",
            "type": "string"
        },
        {
            "name": "relevance",
            "type": "float"
        },
        {
            "name": "ncc_flag",
            "type": "string"
        },
        {
            "name": "published_at",
            "type": "string"
        },
        {
            "name": "use_flag",
            "type": "string"
        }
   
    ]
}
```



# msk connect 

```json
key.converter.region=ap-northeat-2
value.converter.region=ap-northeat-2
key.converter.schemaAutoRegistrationEnabled=true
value.converter.schemaAutoRegistrationEnabled=true
key.converter.avroRecordType=GENERIC_RECORD
value.converter.avroRecordType=GENERIC_RECORD

```

# boto3 glue schema registry

[boto3 glue](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html)

- schema registry list
- 
```py

import boto3
from pprint import pprint

glue_client = boto3.client('glue', region_name = 'ap-northeast-2')

response = glue_client.list_registries(
    MaxResults=23
)
# pprint(response)
df = pd.DataFrame(response['Registries'])
display(df)

```

- schema list
  
```py
response = glue_client.list_schemas()
df_schema = pd.DataFrame(response['Schemas'])
display(df_schema)
```

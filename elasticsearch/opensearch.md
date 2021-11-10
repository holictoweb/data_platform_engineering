[elastic serch 라이센스 관련](https://aws.amazon.com/ko/blogs/opensource/stepping-up-for-a-truly-open-source-elasticsearch/)

# opensearch 실행

- kibana -> opensearh dashboard

[opensearch document](https://opensearch.org/docs/latest/clients/logstash/index/)

# logstash

[lodading data into aws opensearch service with logstash](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-logstash.html)



## logstash config



#### Logstash.yml

- 로그 스테이시 실행을 컨트롤하는 setting파일

- 다른 설정 말고 초기 설정은 아래와 같이 우선 2가지만 세팅되어 있다.

```yaml
path.data : /var/lib/logstash
path.logs : /var/log/logstash
```

#### jvm.option

- 이 파일을 통해 힙 사이즈를 조절할 수 있다. 초기 세팅은 아래와 같다

```yaml
# 초기 total heapsize
-Xms1g 

# 최대 heap size
-Xmx1g
```

 

#### Pipline.yml

- 현재는 단일 파이프라인으로 구성되어 있다.
- 하나의 인스턴스에서 여러 개의 파이프라인을 실행할 경우 추가해준다.
- 현재는 /etc/logstash/con.d 밑에 있는 .conf 파일로 연결되어있다.

```yaml
- pipeline.id: main
  path.config: "/etc/logstash/conf.d/*.conf"
```



#### conf.d/custom.conf

conf 파일명은 원하는 대로 설정해주면 된다. 위 pipline.yml 파일에서 직접 지정해서 작성하거나 *. conf로 작성한다.





_ _ _

# logstash 설치 

- tar 기반 설치 
- [설치 공식 문서](https://opensearch.org/docs/latest/clients/logstash/index/)

```bash
# tar 파일 다운로드 
wget https://artifacts.opensearch.org/logstash/logstash-oss-with-opensearch-output-plugin-7.13.2-linux-x64.tar.gz

# tar 압축 해제
 tar -zxvf logstash-oss-with-opensearch-output-plugin-7.13.2-linux-x64.tar.gz 

```

- docker 기본 이미지 

```bash
 # docker 설치 
 docker pull opensearchproject/logstash-oss-with-opensearch-output-plugin:7.13.2

docker run -it --rm --name logstash --net test opensearchproject/logstash-oss-with-opensearch-output-plugin:7.13.2 -e 'input { stdin { } } output {
   opensearch {
     hosts => ["https://search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com/"]
     index => "opensearch-logstash-docker-%{+YYYY.MM.dd}"
     user => "aicel"
     password => "Aicel2021!"
     ssl => true
     ssl_certificate_verification => false
   }
 }'
 
# local test 진행
docker run -it --rm 10357402252c -e 'input { stdin { } } output {
   opensearch {
     hosts => ["https://search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com:443"]
     index => "test"
     user => "aicel"
     password => "Aicel2021!"
   }
 }'
 
```



- aws opensearh 연동을 위한 내용 확인 필요 

| OpenSearch           |                     |                |                                                              |
| :------------------- | :------------------ | :------------- | :----------------------------------------------------------- |
| Logstash OSS version | Compatibility mode* | Authentication | Output plugin                                                |
| 7.13.x and lower     | Enabled or disabled | Basic          | [logstash-output-opensearch](https://github.com/opensearch-project/logstash-output-opensearch) |
|                      | Enabled             | IAM            | [logstash-output-amazon_es](https://github.com/awslabs/logstash-output-amazon_es) |
|                      | Disabled            | IAM            | Not supported                                                |

```bash
# install plugin IAM을 사용 하는 경우에 사용 
bin/logstash-plugin install logstash-output-amazon_es

# basic auth 사용 시 plugin
bin/logstash-plugin install logstash-output-opensearch

# mongodb 연동을 위한 plugin
bin/logstash-plugin install logstash-input-mongodb

```



- basic 인증 ( id/pw) 사용 시 아래 config 적용 하여 실행 
- container 사용 시 해당 내용을 -e 환경 변수로 지정 시 자동 실행 
- security 에서 IAM 을 사용 할 경우 해당 accesskey 와 secreet key로 접근 시도
- 접속 IP로 설정 한 경우 IP 확인 

```yaml
input {
  stdin{}
}

output {
  opensearch {
    hosts => ["https://search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com:443"]
    index => "dev"
    user => "aicel"
    password => "pass"
  }
}
```



- connection test

```
https://aicel:"Aicel2021!"@search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com:443
```



# logstash 실행

```bash
# config 파일과 함게 실행 
logstash -f ~/config/logstash.conf

# env 등록이 되어 있지 않은 경우 
bin/logstash -f ~/logstash/config/logstash.conf
```



## 실행 결과 확인

```python
# 결과 확인
curl https://search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com/{inex_name}/_search?pretty

```



# plug-in 리스트

```bash
bin/logstash-plugin list
```



# 한글 색인

```
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
{"acknowledged":true}

```



# jdbc connect



```json
input {
  jdbc {
    jdbc_driver_library => "mysql-connector-java-5.1.36-bin.jar"
    jdbc_driver_class => "com.mysql.jdbc.Driver"
    jdbc_connection_string => "jdbc:mysql://localhost:3306/mydb"
    jdbc_user => "mysql"
    parameters => { "favorite_artist" => "Beethoven" }
    schedule => "* * * * *"
    statement => "SELECT * from songs where artist = :favorite_artist"
  }
}
```



# AWS documentdb jdbc driver

https://github.com/aws/amazon-documentdb-jdbc-driver/releases











_ _ _

>  아래 사항들은 최종 성공은 하지 못함. 

# mongodb connect

- logstash 에서 mongodb 연결

- pymongo connection

```python
moongocon = MongoClient(
            host='tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com',
            port=27017,
            username='root',
            password='01234567890',
            retryWrites=False,
        )
```



[es documenet jdbc connect](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-jdbc.html#plugins-inputs-jdbc-jdbc_password)

```json
input {
  jdbc {
    jdbc_driver_library => "mongojdbc1.2.jar"
    jdbc_driver_class => "com.dbschema.MongoJdbcDriver"
    jdbc_connection_string => "jdbc:mongodb://tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017/naver_news"
    jdbc_user => "root"
    jdbc_password => "01234567890"
    statement => "db.naver_news.find().limit(100);"
  }
}
```

```json

# https://dev-whoan.xyz/19


# Sample Logstash configuration for receiving # UDP syslog messages over port 514 
input { 
    mongodb { 
       uri => 'mongodb://root:01234567890@tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017/db' 
       placeholder_db_dir => '../' 
       placeholder_db_name => 'logstash_sqlite.db'
       collection => 'naver_news' 
       batch_size => 1000 
       parse_method => "simple" 
      } 
} 

filter { mutate { copy => { "_id" => "[@metadata][_id]"} remove_field => ["_id"] } } 

output { elasticsearch 
        { 
         hosts => ["엘라스틱 서치 주소"] 
		index => "데이터를 삽입할 index 명" 
		document_id => "%{[@metadata][_id]}" } 
stdout { } }

```

# jdbc 연결

```yaml
# Sample Logstash configuration for creating a simple
# Beats -> Logstash -> Elasticsearch pipeline.



input {
  jdbc {
    jdbc_driver_library => "/home/ubuntu/logstash/logstash-core/lib/jars/mongojdbc3.1.jar"
    jdbc_driver_class => "Java::com.dbschema.MongoJdbcDriver"
    jdbc_connection_string => "jdbc:mongodb://root:01234567890@tf-dev-docdb-cluster-vst.cluster-c6btgg8fszdb.ap-northeast-2.docdb.amazonaws.com:27017/db"
    jdbc_user => "root"
    jdbc_password => "01234567890"
    statement => "db.naver_news.find({},{'_id': false});"
  }
}


output {
  stdout {
      codec => rubydebug
  }
  opensearch {
    hosts => ["https://search-aicel-dev-opensearch-atjh5v2uxhbyirzplkdeshaguu.ap-northeast-2.es.amazonaws.com:443"]
    index => "mongo"
    user => "aicel"
    password => "Aicel2021!"
  }
}


```

```bash
bin/logstash -f ~/logstash/config/logstash_mongo_jdbc.conf
```

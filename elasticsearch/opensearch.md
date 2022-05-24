[elastic serch 라이센스 관련](https://aws.amazon.com/ko/blogs/opensource/stepping-up-for-a-truly-open-source-elasticsearch/)

# opensearch 실행

- kibana -> opensearh dashboard

[opensearch document](https://opensearch.org/docs/latest/clients/logstash/index/)

# indices 확인

```json
GET _cat/indices?v

health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   dart_report_search_all          ZLHN4DcWQIuEWRsD9bV6Fw   5   1       1000            0    246.5mb        246.5mb


```

- pri 가 shard 넘버 이며 해당 shard 에 저장... 실제 

# thread pool 확인 

```py
# thread pool 확인 
GET /_cat/thread_pool


# 전체 정보 확인 
GET /_cat/thread_pool/?v&h=id,name,active,queue,rejected,completed,size,type&pretty

id                     name                                   active rejected completed size type
Q2xBBpBPRy2lI2GztEo2tg ad-batch-task-threadpool                    0        0         0      scaling
Q2xBBpBPRy2lI2GztEo2tg ad-threadpool                               0        0         0      scaling
Q2xBBpBPRy2lI2GztEo2tg analyze                                     1        0      2602    1 fixed


# hot 상태 인 thoread 확인
GET /_nodes/hot_threads

```





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











_ _ _

>  아래 사항들은 최종 성공은 하지 못함. 

```bash
bin/logstash -f ~/logstash/config/logstash_mongo_jdbc.conf
```


# packages
## user words
- user words 업로드 후 적용 방법. 
- https://docs.aws.amazon.com/ko_kr/opensearch-service/latest/developerguide/custom-packages.html
```py
opensearch = boto3.client('opensearch')

print(package_id, bucket_name, s3_key)
3response = opensearch.update_package(
    PackageID= package_id,
    PackageSource={
        'S3BucketName': bucket_name,
        'S3Key': s3_key
    }
)


```

## 최초 package 등록 방법 
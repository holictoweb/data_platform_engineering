


# kafka ui
- github https://github.com/provectus/kafka-ui
```bash
docker run -p 9090:8080 \
	-e KAFKA_CLUSTERS_0_NAME=aicel-msk-prod \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=b-1.aicelkafkaprod.v6zsge.c2.kafka.ap-northeast-2.amazonaws.com:9092 \
	-d provectuslabs/kafka-ui:latest 

```





```log
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,532] INFO [aicel-avro-test|task-0] Using JDBC dialect MySql (io.confluent.connect.jdbc.source.JdbcSourceTask:127)
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,533] INFO [aicel-avro-test|task-0] Attempting to open connection #1 to MySql (io.confluent.connect.jdbc.util.CachedConnectionProvider:79)
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,536] INFO [aicel-avro-test|task-0] [Producer clientId=connector-producer-aicel-avro-test-0] Cluster ID: vCseWqGyRjKF2ig6Dm-YAg (org.apache.kafka.clients.Metadata:279)
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,575] INFO [aicel-avro-test|task-0] No offsets found for '`news`.`gn_news_company_table`', so using configured timestamp 1660290924000 (io.confluent.connect.jdbc.source.JdbcSourceTask:345)
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,575] INFO [aicel-avro-test|task-0] Started JDBC source task (io.confluent.connect.jdbc.source.JdbcSourceTask:296)
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,575] INFO [aicel-avro-test|task-0] WorkerSourceTask{id=aicel-avro-test-0} Source task finished initialization and start (org.apache.kafka.connect.runtime.WorkerSourceTask:233)
2022-08-12T16:55:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:55:24,576] INFO [aicel-avro-test|task-0] Begin using SQL query: SELECT * FROM `news`.`gn_news_company_table` WHERE `news`.`gn_news_company_table`.`published_at` > ? AND `news`.`gn_news_company_table`.`published_at` < ? ORDER BY `news`.`gn_news_company_table`.`published_at` ASC (io.confluent.connect.jdbc.source.TableQuerier:179)
2022-08-12T16:56:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:56:24,516] INFO [aicel-avro-test|task-0|offsets] WorkerSourceTask{id=aicel-avro-test-0} Committing offsets (org.apache.kafka.connect.runtime.WorkerSourceTask:485)
2022-08-12T16:56:24.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:56:24,516] INFO [aicel-avro-test|task-0|offsets] WorkerSourceTask{id=aicel-avro-test-0} flushing 0 outstanding messages for offset commit (org.apache.kafka.connect.runtime.WorkerSourceTask:502)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:57:04,754] INFO [aicel-avro-test|task-0] WorkerSourceTask{id=aicel-avro-test-0} Committing offsets (org.apache.kafka.connect.runtime.WorkerSourceTask:485)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:57:04,755] INFO [aicel-avro-test|task-0] WorkerSourceTask{id=aicel-avro-test-0} flushing 0 outstanding messages for offset commit (org.apache.kafka.connect.runtime.WorkerSourceTask:502)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] [2022-08-12 07:57:04,755] ERROR [aicel-avro-test|task-0] WorkerSourceTask{id=aicel-avro-test-0} Task threw an uncaught and unrecoverable exception. Task is being killed and will not recover until manually restarted (org.apache.kafka.connect.runtime.WorkerTask:191)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] org.apache.kafka.connect.errors.ConnectException: Tolerance exceeded in error handler
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.errors.RetryWithToleranceOperator.execAndHandleError(RetryWithToleranceOperator.java:206)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.errors.RetryWithToleranceOperator.execute(RetryWithToleranceOperator.java:132)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.WorkerSourceTask.convertTransformedRecord(WorkerSourceTask.java:316)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.WorkerSourceTask.sendRecords(WorkerSourceTask.java:342)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.WorkerSourceTask.execute(WorkerSourceTask.java:256)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.WorkerTask.doRun(WorkerTask.java:189)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.WorkerTask.run(WorkerTask.java:238)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:515)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at java.base/java.lang.Thread.run(Thread.java:829)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] Caused by: org.apache.kafka.connect.errors.DataException: Converting Kafka Connect data to byte[] failed due to serialization error:
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.kafkaconnect.AWSKafkaAvroConverter.fromConnectData(AWSKafkaAvroConverter.java:97)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.storage.Converter.fromConnectData(Converter.java:63)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.WorkerSourceTask.lambda$convertTransformedRecord$3(WorkerSourceTask.java:316)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.errors.RetryWithToleranceOperator.execAndRetry(RetryWithToleranceOperator.java:156)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at org.apache.kafka.connect.runtime.errors.RetryWithToleranceOperator.execAndHandleError(RetryWithToleranceOperator.java:190)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	... 11 more
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] Caused by: com.amazonaws.services.schemaregistry.exception.AWSSchemaRegistryException: Exception occurred while fetching or registering schema definition = {"type":"record","name":"gn_news_company_table","fields":[{"name":"news_url_md5","type":"string"},{"name":"company_code","type":"string"},{"name":"relevance","type":["null",{"type":"bytes","scale":2,"precision":5,"connect.version":1,"connect.parameters":{"scale":"2","connect.decimal.precision":"5"},"connect.name":"org.apache.kafka.connect.data.Decimal","logicalType":"decimal"}],"default":null},{"name":"ncc_flag","type":["null",{"type":"int","connect.type":"int8"}],"default":null},{"name":"published_at","type":{"type":"long","connect.version":1,"connect.name":"org.apache.kafka.connect.data.Timestamp","logicalType":"timestamp-millis"}},{"name":"use_flag","type":["null",{"type":"int","connect.type":"int8"}],"default":null}],"connect.name":"gn_news_company_table"}, schema name = news.naver.gn_news_company_table
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.SchemaByDefinitionFetcher.getORRegisterSchemaVersionId(SchemaByDefinitionFetcher.java:99)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.serializers.GlueSchemaRegistrySerializationFacade.getOrRegisterSchemaVersion(GlueSchemaRegistrySerializationFacade.java:86)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.serializers.avro.AWSKafkaAvroSerializer.serialize(AWSKafkaAvroSerializer.java:115)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.kafkaconnect.AWSKafkaAvroConverter.fromConnectData(AWSKafkaAvroConverter.java:95)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	... 15 more
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] Caused by: com.amazonaws.services.schemaregistry.exception.AWSSchemaRegistryException: Failed to get schemaVersionId by schema definition for schema name = news.naver.gn_news_company_table
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.AWSSchemaRegistryClient.getSchemaVersionIdByDefinition(AWSSchemaRegistryClient.java:148)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.SchemaByDefinitionFetcher$SchemaDefinitionToVersionCache.load(SchemaByDefinitionFetcher.java:110)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.SchemaByDefinitionFetcher$SchemaDefinitionToVersionCache.load(SchemaByDefinitionFetcher.java:106)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache$LoadingValueReference.loadFuture(LocalCache.java:3529)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache$Segment.loadSync(LocalCache.java:2278)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache$Segment.lockedGetOrLoad(LocalCache.java:2155)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache$Segment.get(LocalCache.java:2045)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache.get(LocalCache.java:3951)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache.getOrLoad(LocalCache.java:3974)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.google.common.cache.LocalCache$LocalLoadingCache.get(LocalCache.java:4935)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.SchemaByDefinitionFetcher.getORRegisterSchemaVersionId(SchemaByDefinitionFetcher.java:74)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	... 18 more
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] Caused by: com.amazonaws.services.schemaregistry.exception.AWSSchemaRegistryException: Schema Found but status is FAILURE
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.AWSSchemaRegistryClient.returnSchemaVersionIdIfAvailable(AWSSchemaRegistryClient.java:195)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	at com.amazonaws.services.schemaregistry.common.AWSSchemaRegistryClient.getSchemaVersionIdByDefinition(AWSSchemaRegistryClient.java:145)
2022-08-12T16:57:04.000+09:00	[Worker-0edd124bfd4e106ce] 	... 28 more

```
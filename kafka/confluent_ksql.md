# ksql

[line ksetl 사용 ][https://www.youtube.com/watch?v=9p0J3yZyXeg]


```sql

-- 기본 조회
show tables
show topics


```


# table / stream 생성
- CREATE STREAM/TABLE (from a topic)
- CREATE STREAM/TABLE AS SELECT (from existing streams/tables)
- SELECT (non-persistent query)

```sql
-- create table (topic 생성되어 있어야함.)
CREATE OR REPLACE STREAM random (
  	radom_string varchar,
	radom_numeric varchar
)
WITH (
    kafka_topic='test-ksqldb', 
    value_format='JSON'
);

-- table 생성 




```


# windows
- Tumbling은 자신이 원하는 기간을 딱 정해서 partition을 나누는 것 10초 단위로 windowing(partition)이 된다고 하면 1~10, 11~20 초 이렇게 딱딱 나눠지는 것이라고 보면 됩니다.
- Hopping은 자신이 원하는 만큼의 duration을 정하는 것이라고 보면 됩니다.
- Session은 데이터가 들어오는 단위데로 Partition을 나누는 것입니다. 데이터가 stream형식으로 1~5초 들어왔다가 10초~60초까지 데이터가 들어왔다고 하면 session은 자동으로 1~5 10~60가지 windowing합니다.


# ksal 설치 기본 sample 

```sql
-- From http://docs.confluent.io/current/ksql/docs/tutorials/basics-docker.html#create-a-stream-and-table

-- -- Create a stream pageviews_original from the Kafka topic pageviews, specifying the value_format of DELIMITED
CREATE STREAM pageviews_original (viewtime bigint, userid varchar, pageid varchar) WITH (kafka_topic='pageviews', value_format='DELIMITED');

-- Create a table users_original from the Kafka topic users, specifying the value_format of JSON
CREATE TABLE users_original (registertime BIGINT, gender VARCHAR, regionid VARCHAR, userid VARCHAR) WITH (kafka_topic='users', value_format='JSON', key = 'userid');

-- Create a persistent query by using the CREATE STREAM keywords to precede the SELECT statement
CREATE STREAM pageviews_enriched AS SELECT users_original.userid AS userid, pageid, regionid, gender FROM pageviews_original LEFT JOIN users_original ON pageviews_original.userid = users_original.userid;

-- Create a new persistent query where a condition limits the streams content, using WHERE
CREATE STREAM pageviews_female AS SELECT * FROM pageviews_enriched WHERE gender = 'FEMALE';

-- Create a new persistent query where another condition is met, using LIKE
CREATE STREAM pageviews_female_like_89 WITH (kafka_topic='pageviews_enriched_r8_r9') AS SELECT * FROM pageviews_female WHERE regionid LIKE '%_8' OR regionid LIKE '%_9';

-- Create a new persistent query that counts the pageviews for each region and gender combination in a tumbling window of 30 seconds when the count is greater than one
CREATE TABLE pageviews_regions WITH (VALUE_FORMAT='avro') AS SELECT gender, regionid , COUNT(*) AS numusers FROM pageviews_enriched WINDOW TUMBLING (size 30 second) GROUP BY gender, regionid HAVING COUNT(*) > 1;
```
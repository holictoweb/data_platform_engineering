# datafile 확인



```sql
# 데이터 파일에 직접 접근
sqlite3 logstash_sqlite.db

# database 확인
.databases

# tables 
.tables

# 스키마 정보 확인 
pragma table_info(since_table);
> output
0|table|varchar(255)|0||0
1|place|Int|0||0

# 기본정보가 저장되어 있는 테이블 
sqlite> select * from sqlite_master;


```



```sql
# 테이블 생성
create table since_table ('table' varchar(255), place text);

# 테이블명 변경 


# 칼럼 추가 
alter table mytable add column new_column;


```


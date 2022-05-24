[install mysql](#install-mysql)



# Install MySQL

- 설치 
```bash
# 버젼 확인 
lsb_release -a


# mysql server 설치 - client도 함께 설치 
sudo apt-get install mysql-server

# 설치 후 path 에 대한 부분 확인 필요 

# 보안 관련 설정 ( root 비밀번호 설정 등 )
sudo mysql_secure_installation


```

- 실행 방법 
```bash
# mysql 실행 
sudo systemctl start mysql

# 
sudo /usr/bin/mysql -u root -p

```



# connection 

1. pymysql 연결
```python
import pymysql

#connect = pymysql.connect(host="", port=3306, user="", password="", db="")

connection = pymysql.connect(host='fngo-ml-rds-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com',
                             user='mi_ro',
                             password='aicel2021!',
                             database='news',
                             cursorclass=pymysql.cursors.DictCursor)

# connect 에서 cursor 생성
cursors = connection.cursor()

# SQL문 실행
sql = "select * from news.gn_news_nlp_job where flag='0'"
cursors.execute(sql)

# data fetch
data = cursors.fetchall()
print(data)
# connection 닫기
connection.close()

```

2. sqlalchemy 연결
```py

fngo_con_str = 'mysql+pymysql://fngo:fngofinance@bigfinance-dev.c6btgg8fszdb.ap-northeast-2.rds.amazonaws.com/fngo'
fngo_engine = create_engine(fngo_con_str)
fngo_con = fngo_engine.connect()
# read
df_gn_company = pd.read_sql('select * from gn_company', con=news_con )
# write
df_sync.to_sql(name='gn_{}'.format(table), con=news_con, if_exists='append', index=False)
```   




# USER

```sql

CREATE USER 'aicel'@'%' identified by 'Aicel2021!';


GRANT ALL PRIVILEGES ON *.* TO 'aicel'@'%'

```

- 비밀번호 변경
```sql
-- MySQL 5.7 이상
UPDATE mysql.user SET authentication_string=PASSWORD('Aicel2021!') WHERE User='root' AND Host='localhost';
FLUSH PRIVILEGES;


-- mysql 8.0
alter user 'root'@'lacalhost' identified with mysql_native_password by 'Aicel';

```




# MySQL Management 


```sql
-- 세션 상태 확인 
select count(*) from information_schema.processlist where command='Sleep';



```

# Column 변경

```sql
alter table gn_news_nlp_job add batch_flag tinyint(1) NOT NULL DEFAULT '0'
alter table gn_company add insert_date datetime NOT NULL DEFAULT '20211231'

alter table gn_news_nlp_job drop column batch_flag
```




_ _ _ 


# session check

```sql 
show processlist;
```



# group by concatenate string

```sql
select a.unitygrupnm, GROUP_CONCAT(enppbancmpynm SEPARATOR ', ')
from gn_company_group a
join gn_company_group_overview b
	on a.jurirno = b.crno
group by a.unitygrupcode

select a.unitygrupnm as 'group'
, GROUP_CONCAT( case when c.stock_code is not null then enppbancmpynm end SEPARATOR ',') as 'listed'
, GROUP_CONCAT( case when c.stock_code is null then enppbancmpynm end SEPARATOR ',') as 'private'
-- select * 
from gn_company_group a
join gn_company_group_overview b
    on a.jurirno = b.crno
left outer join gn_company_overview  c
	on a.jurirno = c.jurir_no and c.corp_cls in ('Y', 'K') 
group by a.unitygrupcode
having listed is not null


```



# collation
```sql
```


OperationalError: (1267, "Illegal mix of collations (utf8mb4_0900_ai_ci,IMPLICIT) and (utf8mb4_general_ci,IMPLICIT) for operation '='")







# index 

```sql
CREATE INDEX idx1 ON t1 (column_name ));

DROP INDEX index_name ON tbl_name


```




# DATE

## date 기준 변경 조회
```sql
select DATE_FORMAT(published_at, '%Y-%m-%d %H:%i:%s' )

```

%a	This abbreviation means weekday name. It’s limit is from Sun to Sat.  
%b	This abbreviation means month name. It’s limit is from Jan to Dec.  
%c	This abbreviation means numeric month name. It’s limit is from 0 to 12.  
%D	This abbreviation means day of the month as a numeric value, followed by  suffix like 1st, 2nd, etc.  
%e	This abbreviation means day of the month as a numeric value. It’s limit is  from 0 to 31.  
%f	This abbreviation means microseconds. It’s limit is from 000000 to 999999.  
%H	This abbreviation means hour. It’s limit is from 00 to 23.  
%i	This abbreviation means minutes. It’s limit is from 00 to 59.  
%j	This abbreviation means day of the year. It’s limit is from 001 to 366.  
%M	This abbreviation means month name from January to December.  
%p	This abbreviation means AM or PM.  
%S	This abbreviation means seconds. It’s limit is from 00 to 59.  
%U	This abbreviation means week where Sunday is the first day of the week. It’s limit is from 00 to 53.  
%W	This abbreviation means weekday name from Sunday to Saturday.  
%Y	This abbreviation means year as a numeric value of 4-digits.  



# rownum partition
```sql
select * 
from (
	select DENSE_RANK() over( order by rn.sort_date desc, rn.cluster_id ) as row_rank, rn.*
	from ( 
		select 
		-- case when cl.cluster_id is not null then '2' else '1' end as 'cluster_type', 
		me.news_url_md5, me.title, me.published_at, co.company_code, co.relevance, cl.cluster_id, 
		-- case when cl2.max_date is null then me.published_at else cl2.max_date end sort_date
		case when cl.cluster_id is null then me.published_at else MAX(me.published_at) OVER(PARTITION BY cl.cluster_id) end AS 'sort_date'
		-- select *
		from gn_naver_news_meta me
		join gn_news_company_table_20220412 co
			on me.news_url_md5 = co.news_url_md5
		left outer join gn_news_cluster_20220412_2 cl
			on me.news_url_md5 = cl.news_url_md5
		where co.company_code = '005930' and me.published_at > '20200101'
		order by  sort_date  desc 
	) rn
) rn2
where row_rank between 21 and 30 
```


# temp table 생성 
```sql
create temporary table temp_cluster (INDEX idx_cluster (cluster_id ) ) 
select cluster_id, max(published_at) as 'sort_date'
from gn_news_cluster_20220412
group by cluster_id 

```

Add multiple indexes

This statement shows how to add multiple indexes (note that index names - in lower case - are optional):
```sql
CREATE TEMPORARY TABLE core.my_tmp_table 
(INDEX my_index_name (tag, time), UNIQUE my_unique_index_name (order_number))
SELECT * FROM core.my_big_table
WHERE my_val = 1
Add a new primary key:

CREATE TEMPORARY TABLE core.my_tmp_table 
(PRIMARY KEY my_pkey (order_number),
INDEX cmpd_key (user_id, time))
SELECT * FROM core.my_big_table
Create additional columns
```
You can create a new table with more columns than are specified in the SELECT statement. Specify the additional column in the table definition. Columns specified in the table definition and not found in select will be first columns in the new table, followed by the columns inserted by the SELECT statement.
```sql
CREATE TEMPORARY TABLE core.my_tmp_table 
(my_new_id BIGINT NOT NULL AUTO_INCREMENT,  
PRIMARY KEY my_pkey (my_new_id), INDEX my_unique_index_name (invoice_number))
SELECT * FROM core.my_big_table
Redefining data types for the columns from SELECT
```
You can redefine the data type of a column being SELECTed. In the example below, column tag is a MEDIUMINT in core.my_big_table and I am redefining it to a BIGINT in core.my_tmp_table.
```sql
CREATE TEMPORARY TABLE core.my_tmp_table 
(tag BIGINT,
my_time DATETIME,  
INDEX my_unique_index_name (tag) )
SELECT * FROM core.my_big_table
Advanced field definitions during create
```
All the usual column definitions are available as when you create a normal table. Example:
```sql
CREATE TEMPORARY TABLE core.my_tmp_table 
(id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
value BIGINT UNSIGNED NOT NULL DEFAULT 0 UNIQUE,
location VARCHAR(20) DEFAULT "NEEDS TO BE SET",
country CHAR(2) DEFAULT "XX" COMMENT "Two-letter country code",  
INDEX my_index_name (location))
ENGINE=MyISAM 
SELECT * FROM core.my_big_table
```





# 테이블 별 사이즈 확인 
```sql
 SELECT table_name AS 'TableName',
                 ROUND(SUM(data_length+index_length)/(1024*1024), 2) AS 'All(MB)',
                 ROUND(data_length/(1024*1024), 2) AS 'Data(MB)',
                 ROUND(index_length/(1024*1024), 2) AS 'Index(MB)'
FROM information_schema.tables
where  TABLE_SCHEMA = 'news'
GROUP BY table_name
ORDER BY data_length DESC; 
```
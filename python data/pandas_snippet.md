[pandas document](!https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)
[pandas selecting indexing](!https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-and-selecting-data)



# join 

1. merge 
   
```py

# left outer
df_merge = pd.merge(df_sync, df_gn_company, how='left', on='company_code')


# outer 의 결과는 모든 방향으로 생성 
df_update=pd.merge(df_pivot,df_check,how="outer",indicator=True)
 # display(df_update)
 df_update=df_update[df_update['_merge']=='left_only']
 df_delete=df_update[df_update['_merge']=='right_only']


# example
df_merge_parent = pd.merge(df_holdings, df_overview, how='left', on='jurir_no')
df_merge = pd.merge(df_merge_parent[['stock_name', 'stock_code'] + holdings_columns ], df_overview[['jurir_no', 'stock_name', 'stock_code']], how='left', left_on='cdpny_jurir_no', right_on='jurir_no')
df_merge.rename(columns = {'stock_name_x': 'stock_name', 'stock_code_x': 'stock_code', 'jurir_no_x': 'jurir_no', 'stock_name_y': 'sub_stock_name', 'stock_code_y': 'sub_stock_code'}, inplace = True)
display(df_merge)

```

2, 변경 되거나 추가된 데이터 확인

```py
target_table = ['company', 'company_filters', 'company_whitelist']

for table in target_table:   
   print(f'sync table - {table}')             
   df_sync = pd.read_sql('select * from {}'.format(table), con=fngo_con )
   display(df_sync.head(10))

   if table == 'company':
       # company table은 신규 입력 시 insert_date를 추가 하고 update 시에는 insert_date는 기존 데이터를 유지
       df_gn_company = pd.read_sql('select * from gn_company', con=news_con )
       df_merge = pd.merge(df_gn_company, df_sync, how='outer', on='company_code', indicator=True)
       # 신규 데이터네 대하여 insert_date 저장 
       df_merge.loc[df_merge['_merge'] == 'right_only', 'insert_date'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
       # merge 된 데이터 중에 insert_date는 기존것을 유지 
       column = ['company_code', 'company_name_y', 'company_name_eng_y', 'company_type_y', 'market_type_y', 'is_trading_y', 'last_trade_date_y', 'insert_date']
       
       df_sync = df_merge[column]

   print(len(df_sync))
   news_engine.execute("DELETE FROM gn_{}".format(table))
   # replace는 table을 drop 하기 때문에 delete 후 append
   df_sync.to_sql(name='gn_{}'.format(table), con=news_con, if_exists='append', index=False)


```

# group by
## idxmax 
```py
# max 값의 id를 반환하여 해당 row 조회 
# type 이 numeric이어야함. 
df_result['hits'] = df_result['hits'].astype('int')
print(df_result.dtypes)

display(df_result.loc[df_result.groupby(['private'])["hits"].idxmax()])

```
## concatnate

```py
df.groupby(['name','month'])['text'].apply(','.join).reset_index()

# group by 의 결과는 dict 
group_dict = df_group.groupby(['group','company_type']).apply(lambda x: ','.join(x.company_name))

df_target = pd.DataFrame(group_dict)
display( df_target ) 


```

# display data
```python
# display all data 
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option('display.max_rows', None)


```

## if condition
```py
import pandas as pd

names = {'first_name': ['Jon','Bill','Maria','Emma']}
df = pd.DataFrame(names,columns=['first_name'])

df.loc[df['first_name'] == 'Bill', 'name_match'] = 'Match'  
df.loc[df['first_name'] != 'Bill', 'name_match'] = 'Mismatch'  
 
print (df)
```
- string lambda

```py
import pandas as pd

names = {'first_name': ['Jon','Bill','Maria','Emma']}
df = pd.DataFrame(names,columns=['first_name'])

df['name_match'] = df['first_name'].apply(lambda x: 'Match' if x == 'Bill' else 'Mismatch')

print (df)
```


# function 



# Pivot
- pivot_table
- https://riptutorial.com/pandas/example/4771/pivoting-with-aggregating
```py
import pandas as pd
import numpy as np

df = pd.DataFrame({'Name':['Mary', 'Jon','Lucy', 'Jane', 'Sue', 'Mary', 'Lucy'],
                   'Age':[35, 37, 40, 29, 31, 26, 28],
                   'City':['Boston', 'Chicago', 'Los Angeles', 'Chicago', 'Boston', 'Boston', 'Chicago'],
                   'Position':['Manager','Manager','Manager','Programmer', 'Programmer','Manager','Manager'],
                    'Sex':['Female','Male','Female','Female', 'Female','Female','Female']},
                    columns=['Name','Position','City','Age','Sex'])

print (df)
   Name    Position         City  Age  Sex
0  Mary     Manager       Boston   35  Female
1   Jon     Manager      Chicago   37  Male
2  Lucy     Manager  Los Angeles   40  Female
3  Jane  Programmer      Chicago   29  Female
4   Sue  Programmer       Boston   31  Female
5  Mary     Manager       Boston   26  Female
6  Lucy     Manager      Chicago   28  Female


print (df.pivot_table(index='Position', columns='City', values='Name', aggfunc='first')) 
City       Boston Chicago Los Angeles
Position                             
Manager      Mary     Jon        Lucy
Programmer    Sue    Jane        None

print (df.pivot_table(index='Position', columns='City', values='Name', aggfunc='last')) 
City       Boston Chicago Los Angeles
Position                             
Manager      Mary    Lucy        Lucy
Programmer    Sue    Jane        None

print (df.pivot_table(index='Position', columns='City', values='Name', aggfunc='sum')) 
City          Boston  Chicago Los Angeles
Position                                 
Manager     MaryMary  JonLucy        Lucy
Programmer       Sue     Jane        None

print (df.pivot_table(index='Position', columns='City', values='Name', aggfunc=', '.join)) 
City            Boston    Chicago Los Angeles
Position                                     
Manager     Mary, Mary  Jon, Lucy        Lucy
Programmer         Sue       Jane        None

print (df.pivot_table(index='Position', columns='City', values='Name', aggfunc=', '.join, fill_value='-')
         .reset_index()
         .rename_axis(None, axis=1))
     Position      Boston    Chicago Los Angeles
0     Manager  Mary, Mary  Jon, Lucy        Lucy
1  Programmer         Sue       Jane           -
```

# Unpivot
```py
df_fngo = pd.read_json(df_json['df_fngo_json'], orient ='index')
df_news = pd.read_json(df_json['df_news_json'], orient ='index')


df_pivot = df_fngo.loc[:,['company_code', 'company_name', 'company_name_eng']]
df_pivot['stock_code'] = df_fngo.company_code.str[1:]
# display(df_pivot.head(10))
print(f'total input : {len(df_pivot)}')

df_pivot = df_pivot.melt( id_vars='company_code', var_name= 'keyword_type', value_name= 'keyword')
```

# unpivot with concatenate string
```py
# 특정 컬럼에 대한 concatenate
df_pivot = df_pivot.pivot_table(index='company_code', columns='keyword_type', values='keyword', aggfunc=', '.join).copy()

# 전체 칼럼을 concate 하지만 칼럼 기준에 대한 부분이 좀 애매함
df_pivot = df_pivot.pivot_table(index='company_code', columns='use_flag', values='keyword', aggfunc=', '.join).copy()
```

# exploding list-like column
https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html#exploding-a-list-like-column
```py
df
Out[138]: 
     keys            values
0  panda1    [eats, shoots]
1  panda2  [shoots, leaves]
2  panda3    [eats, leaves]

df.explode("values")
Out[140]: 
     keys  values
0  panda1    eats
0  panda1  shoots
1  panda2  shoots
1  panda2  leaves
2  panda3    eats
2  panda3  leaves
```

## reset index
```python
# slice 한 df의 index를 재 설정
df_save_m.reset_index(drop=True, inplace=True)


```





# CREATE DATAFRAME


```python

# import pandas as pd
import pandas as pd
  
# list of strings
lst = ['Geeks', 'For', 'Geeks', 'is', 'portal', 'for', 'Geeks']
  
# list of int
lst2 = [11, 22, 33, 44, 55, 66, 77]
  
# Calling DataFrame constructor after zipping
# both lists, with columns specified
df = pd.DataFrame(list(zip(lst, lst2)),
               columns =['Name', 'val'])
```

```python
# pandas from dict 

# import pandas as pd
import pandas as pd 
    
# List1 
lst = [['tom', 25], ['krish', 30],
       ['nick', 26], ['juli', 22]]
    
df = pd.DataFrame(lst, columns =['Name', 'Age'])
df
```





# db 데이터 sync

```py
def task_sync_company():
      target_table = ['company', 'company_filters', 'company_whitelist']

      for table in target_table:   
          print(f'sync table - {table}')             
          df_sync = pd.read_sql('select * from {}'.format(table), con=fngo_con )
          display(df_sync.head(10))

          if table == 'company':
              # company table은 신규 입력 시 insert_date를 추가 하고 update 시에는 insert_date는 기존 데이터를 유지
              df_gn_company = pd.read_sql('select * from gn_company', con=news_con )
              df_merge = pd.merge(df_gn_company, df_sync, how='outer', on='company_code', indicator=True)
              # 신규 데이터네 대하여 insert_date 저장 
              df_merge.loc[df_merge['_merge'] == 'right_only', 'insert_date'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

              # new insert target 
              print('New Data : ')
              display( df_merge.loc[df_merge['_merge'] == 'right_only'] )
              # merge 된 데이터 중에 insert_date는 기존것을 유지 
              column = ['company_code', 'company_name_y', 'company_name_eng_y', 'company_type_y', 'market_type_y', 'is_trading_y', 'last_trade_date_y', 'insert_date']
              
              df_sync = df_merge[column]
              df_sync.rename(columns = {'company_name_y':'company_name', 'company_name_eng_y':'company_name_eng', 'company_type_y':'company_type', 'market_type_y':'market_type', 'is_trading_y':'is_trading', 'last_trade_date_y':'last_trade_date'}, inplace=True)
              
          print(len(df_sync))
          news_engine.execute("DELETE FROM gn_{}".format(table))
          df_sync.to_sql(name='gn_{}'.format(table), con=news_con, if_exists='append', index=False)

      return {'result':1}

```
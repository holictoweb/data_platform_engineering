[pandas document](!https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)

# pandas data 추가
```py


```


# data 정보 조회


# display setting
```python
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('mode.chained_assignment',  None)

# df에 바로 적용 
heading_properties = [('font-size', '18px')]
cell_properties = [('font-size', '16px')]

dfstyle = [dict(selector="th", props=heading_properties), dict(selector="td", props=cell_properties)]

df.style.set_table_styles(dfstyle)

# 간단하게 전체에 적용
display(df.style.set_table_attributes('style="font-size: 17px"'))

```

# TYPE/DATA CHANGE
## 1. apply 

- 개별 칼럼에 데이터 변경 적용 
- string 으로 변환 하여 적용 후 칼럼에추가 적용 
```py
df_overview['adres'] = df_overview['adres'].astype(str).apply(lambda x: ' '.join(x.split(' ')[:2]) )


```

## 2. pd.to_datetime
```py
data['Date_Time'] = pd.to_datetime(data['Date_Time'])

df['DataFrame Column'] = pd.to_datetime(df['DataFrame Column'], format='%Y%m%d')



```

# read_csv

```py
import pandas as pd
import boto3
import io

s3_client = boto3.client("s3")

obj = s3_client.get_object(Bucket="nlp-entity-linking-train-set", Key="rsc/company_people.txt")
print (obj)
target_columns = ['stock_code', 'info']
df_people = pd.read_csv(io.BytesIO(obj["Body"].read()), sep='\t', header=None, names=target_columns, dtype={'stock_code':str,'info':str}  )

df_people['info']  = df_people['info'].astype(str).apply(lambda x : x.replace('"', '').replace('[', ' ').replace(']', ' ') )
display(df_people)
```

# json dict 처리 

```python 
import pandas as pd
jsonStr = '''{"Index0":{"Courses": "Pandas","Discount": "1200"},
           "Index1":{"Courses": "Hadoop","Discount": "1500"},
           "Index2":{"Courses": "Spark","Discount": "1800"}
          }'''
# Convert JSON to DataFrame Using read_json()
df2 = pd.read_json(jsonStr, orient ='index')
print(df2)



import pandas as pd
import json
from pandas import json_normalize
json_string = '{ "Courses": "Spark", "Fee": 22000,"Duration":"40Days"}'
data = json.loads(json_string)

# Use pandas.DataFrame.from_dict() to Convert JSON to DataFrame
df2 = pd.DataFrame.from_dict(data, orient="index")
print(df2)


# to_json

df.to_json('test.json', orient='table')



```
# select 
### 1. column 선택

```python
data = {"names": ["Kilho", "Kilho", "Kilho", "Charles", "Charles"],
           "year": [2014, 2015, 2016, 2015, 2016],
           "points": [1.5, 1.7, 3.6, 2.4, 2.9]}
df = pd.DataFrame(data, columns=["year", "names", "points", "penalty"],
                          index=["one", "two", "three", "four", "five"])
df

# column 선택
df['year']
df.year


# multi column 선택
df[['year','points']]

```


### 2. row 선택 
```python
# 0 ~ 2번째 row 선택 ( index 와 상관없는 rownumn 으로 조회 하는 형태 )
df[0:3]

# loc 은 index column 정보를 가지고 옴
# index 를 선택 할 수 있지만 반환 형태가 series로 반환 
df.loc['two']

# index two 에서 four 까지를 조회 하며 points 칼럼을 조회 
df.loc['two':'four', 'points']

# row 에 대한 선택이 없이 column을 선택하는것
df.loc[:,'year'] # == df['year']
df.loc[:,['year','names']]


# row와 column 을 모두 index 기반으로 조회 
df.iloc[3:5, 0:2]
df.iloc[[0,1,3], [1,2]]

```


# where 
## row 선택
```python
# year가 2014보다 큰 boolean data
df.loc[df['year']>2014,:]

df.loc[df['names'] == 'Kilho',['names','points']]
df.loc[(df['points']>2)&(df['points']<3),:]


df.loc
```


# data 추가/삭제 
### 1. column 추가/삭제

```python
# column 에 default 값 설정
df['penalty'] = 0.5

# index 순서대로 data 삽입
df['penalty'] = [0.1, 0.2, 0.3, 0.4, 0.5]

# seriese 형태로 삽입
val = pd.Series([-1.2, -1.5, -1.7], index=['two','four','five'])
df['debt'] = val


# 값을 변경 하여 추가 
df['net_points'] = df['points'] - df['penalty']


df.loc[len(df.index)] = [value1, value2, value3, ...]

```

```python
# 칼럼 삭제 
del df['high_points']
```


### 2. row 추가/삭제
```python
df.loc['six',:] = [2013,'Jun',4.0,0.1,2.1]
df.loc[len(df.index)] = [value1, value2, value3, ...]

# existing dataframe add
df = df.append(df2, ignore_index = True)


```


- - -

```python
# nan값인지 확인하기
df.isnull()

df.sum(axis=0)


```





# append dataframe

## concat
```python

df_row_reindex = pd.concat([df1, df2], igonore_index = True)


```

- row 단위로 데이터 추가

```python

# list -> dataframe

df.loc[len(df)] = ['list','data']

# dict -> dataframe
output = pd.DataFrame()
output = output.append(dictionary, ignore_index=True)
print(output.head())

```




# index 설정

```python
# 기존 인덱스 삭제
df_save_m.reset_index(drop=True, inplace=True)

# 인덱스 였던 컬럼을 그대로 살리고 새로 인덱스 생성 
df_save_m.reset_index(inplace=True)

```





# iteration

**DataFrame.iterrows()**

**DataFrame.iteritems() **

**DataFrame.itertuples()**

![](https://t1.daumcdn.net/cfile/tistory/99693846600414F413)



```
for i in df.index: 

```




# datetime 

```py


```
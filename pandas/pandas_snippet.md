[pandas document](!https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)
[pandas selecting indexing](!https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-and-selecting-data)


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


## reset index
```python
# slice 한 df의 index를 재 설정
df_save_m.reset_index(drop=True, inplace=True)

# 

```



# CREATE DATAFRAME


```py

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

```py
# pandas from dict 

# import pandas as pd
import pandas as pd 
    
# List1 
lst = [['tom', 25], ['krish', 30],
       ['nick', 26], ['juli', 22]]
    
df = pd.DataFrame(lst, columns =['Name', 'Age'])
df
```
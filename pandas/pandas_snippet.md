[pandas document](!https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)
[pandas selecting indexing](!https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-and-selecting-data)


# display data
```python
# display all data 
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option('display.max_rows', None)


```




# function 


## reset index
```python
# slice 한 df의 index를 재 설정
df_save_m.reset_index(drop=True, inplace=True)

# 

```



# empty check 
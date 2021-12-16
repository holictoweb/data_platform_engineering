





# 1. TA lib 설치

https://ta-lib.org/ 에서 설치 파일 확인 https://ta-lib.org/hdr_dw.html 다운로드

https://ta-lib.org/function.html

 [ta-lib-0.4.0-src.tar.gz](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz)

 

```bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/

# c compiler 
sudo apt-get install gcc

./configure --prefix=/usr

# 추가 설치
sudo apt install make

make
sudo make install

# python wrapper
pip install TA-Lib
```



# 2. data 추출



```python
import talib 
import talib.abstract as ta


df['avg'] = ta.ADX(df['High'],df['Low'], df['Close'], timeperiod=20)
```



# 3. zeppelin 데이터 display

```python

algo_type = z.select('algo', [('B1', 'algo b1'),('B2', 'algo b2')], 'algo b1')
condition = z.select('condition', [('a', 'all'),('m', 'minus'),('p', 'plus')], 'all')
today = z.input("date")

ORDER_COLUMS = ['date', 'code','buy', 'sell', 'sell_time', 'delta', 'ratio',  'status', ]
NUMERIC_COLUMNS = ['algo', 'macd', 'macds','macdh','rsi_6', 'rsi_6_1','rsi_6_2',  'rsi_14', 'vr', 'voma3_ra', 'voma20_ra', 'clma3_ra', 'clma20_ra', 'pdi','pdi_1','pdi_2', 'mdi', 'mdi_1', 'mdi_2', 'adx','adxr','adxr_1','adxr_2']

# today = datetime.today().strftime('%Y%m%d')
order_file = '../data/order_' +today+'.csv' 

df_check = pd.read_csv(order_file)
df_check.astype({"ratio":float})

mask = (df_check.algo == algo_type)

if condition == 'p':
    mask = mask & (df_check.ratio >= 0.00)
elif condition == 'm':
    mask = mask & (df_check.ratio < 0.00)


df_check = df_check.loc[mask]
# display(df_check[ORDER_COLUMS + NUMERIC_COLUMNS])

total_ratio = 1
for idx, row in df_check.iterrows():
    total_ratio = round(total_ratio * (1 + row['ratio']/100), 5)

print(f'[total] : {total_ratio}, len : {len(df_check)}')



# print(df_check[ORDER_COLUMS + NUMERIC_COLUMNS])
df_dict = df_check[ORDER_COLUMS + NUMERIC_COLUMNS].to_dict(orient='records')
# print(df_dict)
z.z.angularBind("data_bind", df_dict)
z.z.angularBind("order_columns", ORDER_COLUMS)
z.z.angularBind("numeric_columns", NUMERIC_COLUMNS)

print('''
%angular
<script type="text/javascript">
var scope = angular.element(element.parent('.ng-scope')).scope().compiledScope;
</script>

<div  style="height: 600px;overflow-y: scroll; font-size: 0.8em; ">
    <table class="table table-hover">
        <thead class="thead-light">
            <tr>
                <th scope="col">#</th>
                <th ng-repeat="col in order_columns"  scope="col">{{col}}</th>
                <th ng-repeat="col in numeric_columns"  scope="col">{{col}}</th>
            </tr>
        </thead>
        <tbody>
            <tr ng-repeat="obj in data_bind" ng-click="z.runParagraph('paragraph_1639033720545_1709173533'); z.angularBind('data', obj , 'paragraph_1639033720545_1709173533');">
                <td>{{$index + 1}}</td>
                <td ng-repeat="col in order_columns"  scope="col">{{obj[col]}}</td>
                <td ng-repeat="col in numeric_columns"  scope="col">{{obj[col] | number : 2}}</td>
            </tr>
        </tbody>
    </table>
    <hr />
</div>
''')


```


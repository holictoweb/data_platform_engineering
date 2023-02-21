- zeppelin docs 

https://new-docs.zepl.com/docs/using-the-zepl-notebook/develop/zepl-commands



# 1. Dynamic form 

```json
# sql 에서 사용 
%fngo
use news;
select * from gn_keywords where keyword = '${keyword name}';
```

- python

```python
query_input = z.textbox("search keyword")
query_count = z.select("query count", [("20","20"), ("50","50"), ("100","100"), ("200","200")] )

# select default 값 지정
target_index = z.select("target_index", [("dart_report_2", "dart_report_2"), ("dart_report_words", "dart_report_words")], "dart_report_2")


# checkbox
options = [("apple","Apple"), ("banana","Banana"), ("orange","Orange")]
print("Hello "+ " and ".join(z.checkbox("fruit", options, ["apple"])))


```



# 2. angular

- button call other paragraph

```html
%angular
<form class="form-inline">
  <div class="form-group">
    <label for="keyword">Paragraph Id: </label>
    <input type="text" class="form-control" id="keyword" placeholder="keyword ..." ng-model="keyword_model"></input>
  </div>
  <button type="submit" class="btn btn-primary" ng-click="z.angularBind('a',keyword_model,'paragraph_1638324506045_1173930375');z.runParagraph('paragraph_1638324506045_1173930375')"> bind </button>
</form>

```





##  Feature matrix comparisons

|                          Actions                           |                        Front-end API                         |                 Back-end API                 |
| :--------------------------------------------------------: | :----------------------------------------------------------: | :------------------------------------------: |
|                      Initiate binding                      |        z.angularbind(var, initialValue, paragraphId)         |       z.angularBind(var, initialValue)       |
|                        Update value                        | same to ordinary angularjs scope variable, or z.angularbind(var, newValue, paragraphId) |         z.angularBind(var, newValue)         |
|                       Watching value                       |          same to ordinary angularjs scope variable           | z.angularWatch(var, (oldVal, newVal) => ...) |
|                      Destroy binding                       |              z.angularUnbind(var, paragraphId)               |             z.angularUnbind(var)             |
|                    Executing Paragraph                     |                 z.runParagraph(paragraphId)                  |              z.run(paragraphId)              |
| Executing Paragraph (Specific paragraphs in other notes) ( |                                                              |          z.run(noteid, paragraphId)          |
|                       Executing note                       |                                                              |              z.runNote(noteId)               |





# 3. data 

```python
# 동일 셀에서만 적용 
z.put("myVar", "eeeeee")

print(z.get("myVar"))


```



# 4. rest api call

- https://zeppelin.apache.org/docs/0.10.0/usage/rest_api/notebook.html#overview

```python
# prmission 확인
http://3.35.47.225:8081/api/notebook/2GNB26762/permissions
        

# notebook 전체 리스트 확인 
http://3.35.47.225:8081/api/notebook

# notebook 의 paragraph 의 전체 상태 확인
http://3.35.47.225:8081/api/notebook/job/2GNB26762
            
# 특정 paragraph를 수행 
http://3.35.47.225:8081/api/notebook/run/2GNB26762/paragraph_1637025531065_1914305535

http://[zeppelin-server]:[zeppelin-port]/api/notebook/run/[noteId]/[paragraphId]
                
# 특정 notebook 전체 실행
http://3.35.47.225:8081/api/notebook/job/2GQ8JWTVP

# 실제 제대로 돌아 가지는 않음. 

```



_ _ _

# angular display



- 기본적인 input select 값 생성 및 전달 

```html
<form class="form-inline">
            <label class="col-lg-1">Elasticsearch</label>
            <input type="text" class="col-lg-7" id="search_keyword" ng-model="searchText"></input>
            &nbsp
            <select id="query_type" class="form-select" aria-label="Default example" ng-model="searchType">
              <option value="must" selected>and</option>
              <option value="should">or</option>
            </select>
            <button type="submit" class="btn btn-primary" ng-click="z.runParagraph('paragraph_1638238203238_507308036'); z.angularBind('query_input', searchText , 'paragraph_1638238203238_507308036'); z.angularBind('query_type', searchType , 'paragraph_1638238203238_507308036')"> Search</button>
            <!--<button type="submit" class="btn btn-primary" ng-click="z.runParagraph('paragraph_1638344751784_533930122')"> Reset</button>-->
        </form>
```

- angular <-> python 

```python
%python
z.z.angularUnbind("name")
bunny = 'https://positively.com/files/bunny-on-side.jpg'
bunny = 'go home'
z.z.angularBind("name", bunny)

print(z.angular("name"))

print('''
%angular
<h3>{{name}} </h3>

''')
```



- angular scope 가져 오기 

```html
<script type="text/javascript">
var scope = angular.element(element.parent('.ng-scope')).scope().compiledScope;
</script>
```



# angular table

```python
data1 = [ { "name" : "홍길동", "age" : 20 }, { "name" : "강길동", "age" : 21 }, { "name" : "최길동", "age" : 22 } ]
z.z.angularBind("data1", data1)
print('''
%angular
<script type="text/javascript">
var scope = angular.element(element.parent('.ng-scope')).scope().compiledScope;
scope.hello1 = "test angular";
</script>

<div>
</div>

<div>
    <table border="1">
        <tr ng-repeat="obj in data1">
            <td>{{$index + 1}}</td>
            <td ng-if="$odd" style="color:red">{{obj.name}}</td>
            <td ng-if="$even" style="color:black">{{obj.name}}</td>
            <td>{{obj.age}}</td>
        </tr>
    </table>
    <hr />
</div>
''')

# to_html 을 사용 하여 바로 표현 
data1 = df.to_html()
print(data1)
z.z.angularBind("data1", data1)

print('''
%angular
<script type="text/javascript">
var scope = angular.element(element.parent('.ng-scope')).scope().compiledScope;
scope.hello1 = "test angular";
</script>
<div>
    <h3>test : {{hello}}</h3>
    <h3>angular scope : {{hello_1}}</h3>
</div>
''' + data1)
```



# angular table <- df

```python
data1 = df.to_dict(orient='records')
# print(data1)
z.z.angularBind("data1", data1)

print('''
%angular
<script type="text/javascript">
var scope = angular.element(element.parent('.ng-scope')).scope().compiledScope;

</script>

<div  style="height: 600px;overflow-y: scroll; font-size: 0.7em; ">
    <table class="table table-hover">
        <thead class="thead-light">
            <tr>
                <th scope="col">#</th>
                <th scope="col">rcept_no</th>
                <th scope="col">corp_name</th>
                <th scope="col">report_nm</th>
                <th scope="col">term</th>
                <th scope="col">score</th>
                <th scope="col">hits</th>
                <th scope="col">idf</th>
                <th scope="col">tf</th>
                <th scope="col">bootst</th>
            </tr>
        </thead>
        <tbody>
            <tr ng-repeat="obj in data1" ng-click="z.runParagraph('paragraph_1638240458557_304605291'); z.angularBind('query_rcept_no', obj , 'paragraph_1638240458557_304605291');">
                <td>{{$index + 1}}</td>
                <td>{{obj.rcept_no}}</td>
                <td>{{obj.corp_name}}</td>
                <td>{{obj.report_nm}}</td>
                <td>{{obj.term}}</td>
                <td>{{obj.score}}</td>
                <td>{{obj.hits}}</td>
                <td>{{obj.idf}}</td>
                <td>{{obj.tf}}</td>
                <td>{{obj.boost}}</td>
            </tr>
        </tbody>
    </table>

    <hr />
</div>

''')
```



# column 별 처리 포함 

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


# angular

# 1. checkbox
```py

angular_check = '' #초기화
for idx in range(len(keyword_list)):
    checkbox_id = 'check_'+str(idx)
    angular_check = angular_check + f'''
    <div class="form-check form-check-inline col-md-1" style="font-size: 0.7em">
        <input class="form-check-input" type="checkbox" value="" id="{keyword_list[idx]}" onclick="appendSerch('{keyword_list[idx]}')">
        <label class="form-check-label" for="{keyword_list[idx]}">
        {keyword_list[idx]}
        </label>
    </div>
    '''
angular_synonym = '<div class="row col-lg-12">' + angular_check + '</div>' 
```



# 2. datapicker 

```py
date_picker = '''
%angular
<link rel="stylesheet" href="//code.jquery.com/ui/1.12.0/themes/base/jquery-ui.css">
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.0/jquery-ui.js"></script>

<script>
    angular.element( function() {
        angular.element( "#todatepicker" ).datepicker({ dateFormat: 'yy-mm-dd',changeMonth: true,changeYear: true, minDate: new Date(1900, 1, 1), yearRange: '1900:+00' });
        angular.element( "#fromdatepicker" ).datepicker({ dateFormat: 'yy-mm-dd',changeMonth: true,changeYear: true,  minDate: new Date(1900, 1, 1), yearRange: '1900:+00' });
    } );
    
    function changeMaxDate(val){
         angular.element('#fromdatepicker').datepicker('option', 'maxDate', new Date(val));
    }
    
    function changeMinDate(val){
        angular.element('#todatepicker').datepicker('option', 'minDate', new Date(val));
    } 
        
</script>

<form class="form-inline">

    <div style="text-align:center; margin-bottom:20px">
    <button type="submit" class="btn btn-primary"  ng-click="z.runParagraph('20210728-173149_661735685')" > Load data </button>
    </div>

    <div style="text-align:center">

            <label for="fromDateId" >From: </label>
            <input type="text"  id="fromdatepicker" ng-model="fromDate" onChange="changeMinDate(this.value);" autocomplete="off"> </input>
            <label for="toDateId"style="margin-left:5px"> to: </label>
            <input type="text" id="todatepicker" ng-model="toDate" onChange="changeMaxDate(this.value);" autocomplete="off"> </input>

            <label style="margin-left:30px"> City: </label>
            <input type="text" ng-model="city"> </input>

            <label for="genders" style="margin-left:30px">Gender:</label>
            <select name="genders" id="genders" ng-model="gender">
                <option value="both">Both</option>
                <option value="F">Female</option>
                <option value="M">Male</option>
            </select>

    </div>
    <div style="text-align:center; margin-top:20px">
    <button type="submit" class="btn btn-primary" ng-click="z.angularBind('toDate',toDate,'20210727-110725_1586668489');z.angularBind('fromDate',fromDate,'20210727-110725_1586668489');z.angularBind('city',city,'20210727-110725_1586668489');z.angularBind('gender',gender,'20210727-110725_1586668489');z.runParagraph('20210727-110725_1586668489');z.runParagraph('20210727-111144_1584153174')">Search</button>
    </div>
</form>
'''

print(date_picker)

```
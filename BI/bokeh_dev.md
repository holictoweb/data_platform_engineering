



# event handler






# widget
- 버튼, 슬라이더, 차트, 데이트피커 등 설정
https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html


```python
# button click event
button = Button(label="Foo", button_type="success")
button.js_on_click(CustomJS(args={}, code='alert("test");'))

show(button)

```



# datatable

- zeppelin 상에서는 customJS callback 밖에 설정 할 수 없음 
- 
```python

##################################### datatable
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models import CustomJS, TextInput


source = ColumnDataSource(df_table)
Columns = [TableColumn(field=Ci, title=Ci) for Ci in df_table.columns] # bokeh columns

data_table = DataTable(columns=Columns, width=900, editable=True, source=source) # bokeh table

def on_change_data_source(attr, old, new):
    print(source)
    
callback = CustomJS( code="""
    alert('go home!' + carName);
""")

source.selected.js_on_change('indices', callback)
# data_table.source.js_event_callbacks('data', callback)

show(data_table)
```
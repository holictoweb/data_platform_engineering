



# event handler


# tools

```py

tools = ["tap, xzoom_in, xzoom_out, xbox_zoom, xpan, reset"]
```

# stack chart 
- 전체를 vbar_stack 으로 그리는 방식

```py

# Importing library's
from bokeh.plotting import figure, show, output_notebook
import pandas as pd



# Create Students,Subjects list and Colours.
Students = ['Ankur', 'Yash', 'Aditya', 'Harshit']
Subjects = ['Operating System', 'Data Structure',\
            'Java Programming']
cols = ['#00ff00', '#009900', '#00cc99']


# Initialize data to lists.
data = {'Students': Students,
        'Operating System': [17, 20, 19, 18],
        'Data Structure': [19, 18, 20, 17],
        'Java Programming': [20, 19, 20, 18]}
        
# Creates DataFrame.
df = pd.DataFrame(data)
df.head()


fig = figure(x_range=df.Students,
             height=500,
             title="Marks counts of \
             every students according to subjects")
fig.vbar_stack(Subjects,
               x='Students',
               source=df,
               color=cols,
               width=0.5)
show(fig)
```

- 하나씩 직접 그리는 방식 
```py
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.ranges import FactorRange
import pandas as pd

data = [
    ['201720', 'cat1', 20],
    ['201720', 'cat2', 30],
    ['201720', 'cat3', 40],
    ['201721', 'cat1', 20],
    ['201721', 'cat2', 0],
    ['201721', 'cat3', 40],
    ['201722', 'cat1', 50],
    ['201722', 'cat2', 60],
    ['201722', 'cat3', 10],
]

df = pd.DataFrame(data, columns=['week', 'category', 'count'])

display(df)

pt = df.pivot('week', 'category', 'count')

pt = pt.cumsum(axis=1)


display(pt)

output_file("lines.html", title='Dashboard')

p = figure(title="count", x_axis_label='week', y_axis_label='category', x_range = FactorRange(factors=pt.index.tolist()), plot_height=300, plot_width=500)

p.vbar(x=pt.index, bottom=0, top=pt.cat1, width=0.2, color='red', legend_label='cat1')
p.vbar(x=pt.index, bottom=pt.cat1, top=pt.cat2, width=0.2, color='blue', legend_label='cat2')
p.vbar(x=pt.index, bottom=pt.cat2, top=pt.cat3, width=0.2, color='green', legend_label='cat3')
show(p)

```

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


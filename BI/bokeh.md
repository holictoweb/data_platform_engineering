https://docs.bokeh.org/en/latest/docs/reference/document.html





# bokeh install

```bash
pip install bokeh
# zeppelin 에서 사용 하기 위해 필요 
pip install bkzep
```



[Handling categorical data - bokeh doc](https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html)



# bar chart

- basic

```python
from bokeh.io import output_file, show
from bokeh.plotting import figure

output_file("bars.html")

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

p = figure(x_range=fruits, height=250, title="Fruit counts",
           toolbar_location=None, tools="")

p.vbar(x=fruits, top=counts, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
```

- stacking 

```python
from bokeh.io import output_file, show
from bokeh.plotting import figure

output_file("stacked.html")

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
years = ["2015", "2016", "2017"]
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

data = {'fruits' : fruits,
        '2015'   : [2, 1, 4, 3, 2, 4],
        '2016'   : [5, 3, 4, 2, 4, 6],
        '2017'   : [3, 2, 4, 4, 5, 3]}

p = figure(x_range=fruits, height=250, title="Fruit counts by year",
           toolbar_location=None, tools="")

p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
             legend_label=years)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)
```



- basic bar chart

```python
df_con = pd.DataFrame(columns = ['container', 'count'])
# data는 추가로 입력 
source = ColumnDataSource(df_con)
con = source.data['container'].tolist()
p = figure(x_range=con, height=300, y_range=(0, 10))
p.vbar(x='container', top='count', width=0.3, color ='blue', source=source)
p.xgrid.grid_line_color=None

```



## bar chart  hover

- add_tools 

```python
source = ColumnDataSource(df_nk)
xax = source.data['crawled_schedule'].tolist()
p = figure(x_range=xax, plot_width=800, height=300, y_range=(0, 200))
p.vbar(x='crawled_schedule', top='crawled_cnt', width=0.3, color ='blue', source=source)
p.xgrid.grid_line_color=None

# hover 추가
p.add_tools(HoverTool(tooltips = '<font color=blue>cnt:</font><font color=red> @crawled_cnt</font>'))

p.xgrid.grid_line_color = None

# xaxis 기울기 적용 
p.xaxis.major_label_orientation = math.pi / 4  # Rotate axis' labels

p.xaxis.major_label_orientation = "vertical"
```



# line chart (stock)

- http://docs.bokeh.org/en/1.0.2/docs/user_guide/examples/tools_hover_tooltip_formatting.html

```python


import numpy as np

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.sampledata.stocks import AAPL

output_file("tools_hover_tooltip_formatting.html")

def datetime(x):
    return np.array(x, dtype=np.datetime64)

source = ColumnDataSource(data={
    'date'      : datetime(AAPL['date'][::10]),
    'adj close' : AAPL['adj_close'][::10],
    'volume'    : AAPL['volume'][::10],
})

p = figure(plot_height=250, x_axis_type="datetime", tools="", toolbar_location=None,
           title="Hover Tooltip Formatting", sizing_mode="scale_width")
p.background_fill_color="#f5f5f5"
p.grid.grid_line_color="white"
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Price'
p.axis.axis_line_color = None

p.line(x='date', y='adj close', line_width=2, color='#ebbd5b', source=source)

p.add_tools(HoverTool(
    tooltips=[
        ( 'date',   '@date{%F}'            ),
        ( 'close',  '$@{adj close}{%0.2f}' ), # use @{ } for field names with spaces
        ( 'volume', '@volume{0.00 a}'      ),
    ],

    formatters={
        'date'      : 'datetime', # use 'datetime' formatter for 'date' field
        'adj close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                  # use default 'numeral' formatter for other fields
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
))

show(p)
```




# bokeh plot tools

https://docs.bokeh.org/en/latest/docs/user_guide/tools.html

```python

```
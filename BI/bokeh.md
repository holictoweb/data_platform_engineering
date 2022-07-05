https://docs.bokeh.org/en/latest/docs/reference/document.html





# bokeh install

```bash
pip install bokeh

# zeppelin 에서 사용 하기 위해 bkzep 설치
pip install bkzep
```


### bokeh server 설치
```bash


```


[Handling categorical data - bokeh doc](https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html)



# standalonew HTML/JS output
```python
shwo(chart)

```

# bokeh server in zeppelin 
```python

p1 = figure(plot_width=250, plot_height=250)
r1 = p1.circle([1,2,3], [4,5,6], size=20)

t = show(p1, notebook_handle=True)


# File ~/miniconda3/envs/aicel_python/lib/python3.8/site-packages/bkzep/io.py:41, in _show_zeppelin_doc_with_state(obj, state, notebook_handle)
#      39 def _show_zeppelin_doc_with_state(obj, state, notebook_handle):
#      40     if notebook_handle:
# ---> 41         raise ValueError("Zeppelin doesn't support notebook_handle.")
#      42     if _isAfterBokeh1210:
#      43         (script, div, cell_doc) = notebook_content(obj)

ValueError: Zeppelin doesn't support notebook_handle.


```


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


# bokeh on notebook

- https://github.com/bokeh/bokeh/blob/2.4.2/examples/howto/server_embed/notebook_embed.ipynb 



```python


# Embedding a Bokeh server in a Notebook
# This notebook shows how a Bokeh server application can be embedded inside a Jupyter notebook.

import yaml

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

output_notebook()

# There are various application handlers that can be used to build up Bokeh documents. For example, there is a ScriptHandler that uses the code from a .py file to produce Bokeh documents. This is the handler that is used when we run bokeh serve app.py. In the notebook we can use a function to define a Bokehg application.

# Here is the function bkapp(doc) that defines our app:

def bkapp(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25),
                  y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource.from_df(data)

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """, Loader=yaml.FullLoader))

# Now we can display our application using show, which will automatically create an Application that wraps bkapp using FunctionHandler. The end result is that the Bokeh server will call bkapp to build new documents for every new sessions that is opened.

# Note: If the current notebook is not displayed at the default URL, you must update the notebook_url parameter in the comment below to match, and pass it to show.

show(bkapp) # notebook_url="http://localhost:8888" 
 
 

```



# Callback

## CustomJS callback
```python



```
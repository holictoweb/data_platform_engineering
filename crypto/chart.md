# bokeh chart



- 기본적인 차트 표현 

```python
inc = df.close >= df.open
dec = df.open > df.close

p_candlechart = figure(plot_width=1050, plot_height=200, x_range=(-1, len(df)), tools="crosshair")
p_candlechart.segment(df.index[inc], df.high[inc], df.index[inc], df.low[inc], color="red")
p_candlechart.segment(df.index[dec], df.high[dec], df.index[dec], df.low[dec], color="blue")
p_candlechart.vbar(df.index[inc], 0.5, df.open[inc], df.close[inc], fill_color="red", line_color="red")
p_candlechart.vbar(df.index[dec], 0.5, df.open[dec], df.close[dec], fill_color="blue", line_color="blue")


p_volumechart = figure(plot_width=1050, plot_height=100, x_range=p_candlechart.x_range, tools="crosshair")
p_volumechart.vbar(df.index, 0.5, df.volume, fill_color="black", line_color="black")
major_label = {
    i: date.strftime('%Y%m%d %H:%M') for i, date in enumerate(pd.to_datetime(df["date"]))
}
major_label.update({len(df): ''})
p_volumechart.xaxis.major_label_overrides = major_label
# p_volumechart.yaxis[0].formatter = NumeralTickFormatter(format='0,0')


p = gridplot([[p_candlechart], [p_volumechart]], toolbar_location=None)

show(p)

```


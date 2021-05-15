
## matplotlib 한글 깨짐 현상 
- 폰트 시스템 확인
```
import matplotlib.font_manager as fm

font_list = fm.findSystemFonts(fontpaths = None, fontext = 'ttf')

font_list[:]
```


```
##설정 파일 위치 확인
print (mpl.matplotlib_fname())
```

## extension


```
jupyter labextension install @jupyterlab/plotly-extension
```

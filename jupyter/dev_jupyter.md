
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

- extension 설치 환경 설치 
```
pip install jupyter_contrib_nbextensions && jupyter contrib nbextension install 
```

- 설치 관련
```
pip install jupyter_contrib_nbextensions      # 라이브러리 설치
jupyter contrib nbextension install --user    # 쥬피터노트북에서 보일 수 있도록 등록

```
- 설치 확인
```
http://localhost:8888/nbextensions  
```



```
jupyter labextension install @jupyterlab/plotly-extension
```

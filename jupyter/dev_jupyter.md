### jupyter lab 설치 

```python
# 설치 
pip install jupyterlab

# config 파일 생성 
jupyter lab --generate-config
# 아래 위치에 성성
Writing default config to: /home/holictoweb/.jupyter/jupyter_lab_config.py

```

### jupyter lab 외부 접근 

```python

from notebook.auth import passwd
passwd()
Enter password: 
Verify password: 
'sha1:f24baff....' 


```


1. jupyter lab 과 jupyter notebook 의 extension은 별도


- extension 설치 환경 설치 
- jupyter notebook 재시작 
```
pip install jupyter_contrib_nbextensions && jupyter contrib nbextension install 
```


```
- 설치 확인
```
http://localhost:8888/nbextensions  
```
jupyter labextension install @jupyterlab/plotly-extension


```



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
- node.js 설치 
```
conda install -c conda-forge nodejs
```

- check extension tab
- 필요한 extension 설치 


# systemctl 등록


```bash
[Unit]
Description=Jupyter-Notebook Daemon

[Service]
Type=simple
ExecStart=/bin/bash -c "/home/username/.local/share/virtualenvs/notebook/bin/jupyter-notebook --no-browser --notebook-dir=/home/username"
WorkingDirectory=/home/username
User=username
Group=username
PIDFile=/run/jupyter-notebook.pid
Restart=on-failure
RestartSec=60s

[Install]
WantedBy=multi-user.target
```
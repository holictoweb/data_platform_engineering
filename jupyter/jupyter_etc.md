### jupyterhub

1. theme 설정

```
# jupyter 관련 path 확인
jupyter lab path

```



# kernel 등록
- spark 커널 등록에 대한 부분은 추가 확인 필요

```bash
# 커널 등록 (conda 환경 ) 
python -m ipykernel install --user --name={kernelname conda env name}
python -m ipykernel install --user --name bitlab --display-name bitlab
python -m ipykernel install --user --name holic --display-name holic

# drop 커널
jupyter kernelspec uninstall {kernelname}

# 커널 리스트
jupyter kernelspec list
```


# lab extension 설치 

- npm과 nodejs 설치 필요 
```bash
sudo apt install npm


sudo apt install nodejs
# node js 버젼 을 위해서 아래 처럼 설치 필요 
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
source ~/.bashrc
nvm list-remote
nvm install v16.10.0



# 
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

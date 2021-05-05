### jupyterhub

1. theme 설정

```
# jupyter 관련 path 확인
jupyter lab path

```



# kernel 등록
- spark 커널 등록에 대한 부분은 추가 확인 필요

```
# 커널 등록 (conda 환경 ) 
python -m ipykernel install --user --name={kernelname conda env name}

# drop 커널
jupyter kernelspec uninstall {kernelname}

# 커널 리스트
jupyter kernelspec list
```

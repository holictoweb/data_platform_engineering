
# conda 설치 
- 사용할 버젼 확인 
  - https://www.anaconda.com/products/individual#linux
```bash
# miniconda latest 버젼 설치 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 다운 받은 폴더에서 쉘 실행
bash Miniconda3-latest-Linux-x86_64.sh 

Miniconda3 will now be installed into this location:
/home/ubuntu/miniconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/ubuntu/miniconda3] >>> 


# 실행
source ~/.bashrc

# 다른 쉘을 열어서 확인 

```


# cona 환경 구성


```bash
# 기존 환경 복제
conda env export -n [env_name] > environment.yml

# 환경 복제
conda env create -n [new_env_name] -f environment.yml

# 환경 clone
conda create --name holic --clone holic_origin


```



```bash
# zeppelin 환경 등록 
```




# windows conda 구성
- download https://docs.conda.io/en/latest/miniconda.html
- 다운 받아 실행 

```bash


```
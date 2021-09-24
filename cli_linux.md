### Linux

1. find
- 해당 하위 폴더에 특정 구문이 존재 하는 파일 확인 
```
grep "JupyterLab Light" ./*
```




2. linuxstorage 관련



### AWS CLI
1. aws cli 이슈
- 에러 메시지
```
Traceback (most recent call last):
  File "/usr/bin/aws", line 19, in <module>
    import awscli.clidriver
  File "/usr/lib/python3/dist-packages/awscli/clidriver.py", line 36, in <module>
    from awscli.help import ProviderHelpCommand
  File "/usr/lib/python3/dist-packages/awscli/help.py", line 23, in <module>
    from botocore.docs.bcdoc import docevents
ImportError: cannot import name 'docevents' from 'botocore.docs.bcdoc' (/home/ubuntu/.local/lib/python3.8/site-packages/botocore/docs/bcdoc/__init__.py)
```

- python 경로 지정 후 정상 
```
export PYTHONPATH=/usr/local/lib/python3.8/dist-packages/
```



#### superset

```
sudo superset run -p 8088 --with-threads --reload --debugger --host 0.0.0.0
```



## storage

### 스토리지 extend
```bash
# 용량 확인 
df -hT

# 현재 스트리지 구성 확인 
lsblk 


# 용량을 늘려야 할 대상 part 선택 
sudo growpart /dev/nvme0n1 1



```
[]






## vscode 에서 연결 시 

```bash
 # Read more about SSH config files: https://linux.die.net/man/5/ssh_config
 Host aicel-work-airflow
    HostName 54.180.140.218
    User ubuntu
    IdentityFile E:\task\auth\bigfinance.pem
```



## ec2 unprotected private key 



> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
> @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @  
> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
> Permissions for 'E:\\task\\auth\\bigfinance.pem' are too open.  
> It is required that your private key files are NOT accessible by others.  
> This private key will be ignored.  
> Load key "E:\\task\\auth\\bigfinance.pem": bad permissions  


- windows
    - key 파일 (.pem) 우클릭
    - 보안 -> 고급 -> 사용권한 -> 특별히 선택없이 ** 상속 사용 안 함 ** -> 상속된 사용 권한을 이 개체에 대한 명시적 사용 권한으로 변환  선택 
    - user 정보를 모두 삭제하고 현재 Owner로 등록되어 있는 계정만 추가  

![아래 이미지 처럼 처리](https://i.stack.imgur.com/coCbX.gif)
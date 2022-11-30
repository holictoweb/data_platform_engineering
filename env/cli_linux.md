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

### 특정 폴더의 전체 용량 확인
```bash
du -sh pipeline_crawling_nk/

# 하위 폴더의 용량 확인
du -h --max-depth=1 .
```

# cp to ec2

```bash
scp -i myAmazonKey.pem phpMyAdmin-3.4.5-all-languages.tar.gz ec2-user@mec2-50-17-16-67.compute-1.amazonaws.com:~/.
```





# 심볼릭 링크 

```bash
# 링크 생성
ln -s /home/test.txt testlink
# 링크 생성 시 해당 폴더명으로 생성
ln -s /home/testfolder/ testlink

# 링크 삭제 
rm -f testlink

```





# find

```bash
find . -name "test-go.log"
```





# Time Zone 변경 방법
- ubuntu 기준으로 변경 
```bash
# 현재 시간 확인
date

buntu@ip-172-31-15-162:~/data$ sudo dpkg-reconfigure tzdata
debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend requires a screen at least 13 lines tall and 31 columns wide.)
debconf: falling back to frontend: Readline
Configuring tzdata
------------------

Please select the geographic area in which you live. Subsequent configuration questions will narrow this down by presenting a list of cities, representing the time zones 
in which they are located.

  1. Africa   3. Antarctica  5. Arctic Ocean  7. Atlantic Ocean  9. Indian Ocean    11. System V timezones  13. None of the above
[More] 13

  2. America  4. Australia   6. Asia          8. Europe          10. Pacific Ocean  12. US

Geographic area: 6


Please select the city or region corresponding to your time zone.

  1. Aden      11. Baku        21. Damascus          31. Hong Kong  41. Kashgar       51. Makassar      61. Pyongyang  71. Singapore      81. Ujung Pandang
  2. Almaty    12. Bangkok     22. Dhaka             32. Hovd       42. Katmandu      52. Manila        62. Qatar      72. Srednekolymsk  82. Ulaanbaatar
  3. Amman     13. Barnaul     23. Dili              33. Irkutsk    43. Khandyga      53. Muscat        63. Qostanay   73. Taipei         83. Urumqi
  4. Anadyr    14. Beirut      24. Dubai             34. Istanbul   44. Kolkata       54. Nicosia       64. Qyzylorda  74. Tashkent       84. Ust-Nera
  5. Aqtau     15. Bishkek     25. Dushanbe          35. Jakarta    45. Krasnoyarsk   55. Novokuznetsk  65. Rangoon    75. Tbilisi        85. Vientiane
  6. Aqtobe    16. Brunei      26. Famagusta         36. Jayapura   46. Kuala Lumpur  56. Novosibirsk   66. Riyadh     76. Tehran         86. Vladivostok
  7. Ashgabat  17. Chita       27. Gaza              37. Jerusalem  47. Kuching       57. Omsk          67. Sakhalin   77. Tel Aviv       87. Yakutsk
  8. Atyrau    18. Choibalsan  28. Harbin            38. Kabul      48. Kuwait        58. Oral          68. Samarkand  78. Thimphu        88. Yangon
  9. Baghdad   19. Chongqing   29. Hebron            39. Kamchatka  49. Macau         59. Phnom Penh    69. Seoul      79. Tokyo          89. Yekaterinburg
  10. Bahrain  20. Colombo     30. Ho Chi Minh City  40. Karachi    50. Magadan       60. Pontianak     70. Shanghai   80. Tomsk          90. Yerevan

Time zone: 69



Current default time zone: 'Asia/Seoul'
Local time is now:      Fri Dec 31 14:56:38 KST 2021.
Universal Time is now:  Fri Dec 31 05:56:38 UTC 2021.

ubuntu@ip-172-31-15-162:~/data$ 
ubuntu@ip-172-31-15-162:~/data$ 
ubuntu@ip-172-31-15-162:~/data$ date
Fri Dec 31 14:56:42 KST 2021


```


# storage 확인
```bash

```
## airflow 

- airflow start script

```
  1 #! /bin/bash
  2 
  3 echo '------------------------------'
  4 echo '   Starting Airflow Cluster   '
  5 echo '------------------------------'
  6 
  7 sudo kill -9 `pgrep -f airflow`
  8 sudo rm -rf ~/airflow/*.pid
  9 
 10 airflow scheduler -D --stdout ~/airflow/logs/airflow-scheduler.out --stderr ~/airflow/logs/airflow-scheduler.err -l ~/airflow/logs/airflow-scheduler.log
 11 
 12 airflow webserver -D --stdout ~/airflow/logs/airflow-webserver.out --stderr ~/airflow/logs/airflow-webserver.err -l ~/airflow/logs/airflow-webserver.log
 13 
 14 #airflow worker -D --stdout ~/airflow/logs/airflow-worker.out --stderr ~/airflow/logs/airflow-worker.err -l ~/airflow/logs/airflow-worker.log
 15 
 16 airflow flower -D --stdout ~/airflow/logs/airflow-flower.out --stderr ~/airflow/logs/airflow-flower.err -l ~/airflow/logs/airflow-flower.log
 17 
 18 sleep 5
 19 
 20 echo '------------------------------'
 21 echo '   ps -ef | grep airflow      '
 22 echo '------------------------------'
 23 
 24 ps -ef | grep airflow
 25 
```


### scheduler 기동 관련 이슈 사항 

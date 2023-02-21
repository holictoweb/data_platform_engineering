## airflow 

- airflow start script

```bash
#! /bin/bash
 
echo '------------------------------'
echo '   Starting Airflow Cluster   '
echo '------------------------------'

sudo kill -9 `pgrep -f airflow`
sudo rm -rf ~/airflow/*.pid

airflow scheduler -D --stdout ~/airflow/logs/airflow-scheduler.out --stderr ~/airflow/logs/airflow-scheduler.err -l ~/airflow/logs/airflow-scheduler.log

airflow webserver -D --stdout ~/airflow/logs/airflow-webserver.out --stderr ~/airflow/logs/airflow-webserver.err -l ~/airflow/logs/airflow-webserver.log

#airflow worker -D --stdout ~/airflow/logs/airflow-worker.out --stderr ~/airflow/logs/airflow-worker.err -l ~/airflow/logs/airflow-worker.log
 
#airflow flower -D --stdout ~/airflow/logs/airflow-flower.out --stderr ~/airflow/logs/airflow-flower.err -l ~/airflow/logs/airflow-flower.log

sleep 5

echo '------------------------------'
echo '   ps -ef | grep airflow      '
echo '------------------------------'

ps -ef | grep airflow

```


### scheduler 기동 관련 이슈 사항 



## ssh operator
- connector 를 사용 하여 연결 설정 후 EMR에 있는 python 스크립트 수행 
```python
def EMR_ssh_conn(connid,bash_command,dag):
    sshHook = SSHHook(connid)
    ssh_operator = SSHOperator(
        ssh_hook=sshHook,
        task_id=connid,
        command=bash_command,
        dag=dag
    )
    return ssh_operator

ec2_stop_task = EMR_ssh_conn('dev_emr_ssh_conn','python3 /home/hadoop/management/mng_ec2_stop_10min.py',dag)
```


## trigger dag
- retry 를 위해 실패 시 다시 dag 수행 
```python
# Get Task Statue & rest api call external dag
def call_external_dag(**kwargs):
    # Get execution_date
    execution_date = kwargs['execution_date']
    # Get Dag & Task Info
    dag_instance = kwargs['dag']
    operator_instance = dag_instance.get_task("check_prod_to_qa_s3_sync")
    # Task Status
    task_status = TaskInstance(operator_instance, execution_date).current_state()
    if task_status == 'failed':
        # Trigger Dag with REST API
        # result = requests.post(
        #     "http://{}:8080/api/experimental/dags/".format(airflow_master_node_ip) + DAG_NAME + "/dag_runs",
        #     data=json.dumps("{}"),
        #     auth=(airflow_sys_user_id, airflow_sys_user_pwd))
        # pprint(result.content.decode('utf-8'))
        c = Client(None, None)
        c.trigger_dag(dag_id=DAG_NAME, run_id='triggering_rerty_logic_{}'.format(current_time), conf={})
    else:
        pprint(task_status)

retry_logic = PythonOperator(
    task_id='retry_logic',
    provide_context=True,
    python_callable=call_external_dag,
    trigger_rule='all_done',
    dag=dag
)
```

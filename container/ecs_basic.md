# ecs 

___



## boto3 

- [boto3 start_task](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.run_task)

```python

```









___



## airflow ecs operator

- 2.0 부터 ecsoperator 위치 변경 

```python
# sample : https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_modules/airflow/providers/amazon/aws/example_dags/example_ecs_fargate.html

from airflow.providers.amazon.aws.operators.ecs import ECSOperator


```





[ecs operator source code](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_modules/airflow/providers/amazon/aws/operators/ecs.html)

- start_task 소스 
- 현재는 enableExecuteCommand  설정 하는 부분은 없음. ( 소스 추가는 가능 )

```python
def _start_task(self, context):
        run_opts = {
            'cluster': self.cluster,
            'taskDefinition': self.task_definition,
            'overrides': self.overrides,
            'startedBy': self.owner,
        }

        if self.capacity_provider_strategy:
            run_opts['capacityProviderStrategy'] = self.capacity_provider_strategy
        elif self.launch_type:
            run_opts['launchType'] = self.launch_type
        if self.platform_version is not None:
            run_opts['platformVersion'] = self.platform_version
        if self.group is not None:
            run_opts['group'] = self.group
        if self.placement_constraints is not None:
            run_opts['placementConstraints'] = self.placement_constraints
        if self.placement_strategy is not None:
            run_opts['placementStrategy'] = self.placement_strategy
        if self.network_configuration is not None:
            run_opts['networkConfiguration'] = self.network_configuration
        if self.tags is not None:
            run_opts['tags'] = [{'key': k, 'value': v} for (k, v) in self.tags.items()]
        if self.propagate_tags is not None:
            run_opts['propagateTags'] = self.propagate_tags

        response = self.client.run_task(**run_opts)

        failures = response['failures']
        if len(failures) > 0:
            raise ECSOperatorError(failures, response)
        self.log.info('ECS Task started: %s', response)

        self.arn = response['tasks'][0]['taskArn']
        ecs_task_id = self.arn.split("/")[-1]
        self.log.info(f"ECS task ID is: {ecs_task_id}")

        if self.reattach:
            # Save the task ARN in XCom to be able to reattach it if needed
            self._xcom_set(
                context,
                key=self.REATTACH_XCOM_KEY,
                value=self.arn,
                task_id=self.REATTACH_XCOM_TASK_ID_TEMPLATE.format(task_id=self.task_id),
```







# ecs - task definition



- task 정보 조회 

```
aws ecs describe-tasks \
    --cluster dev-aicel-cluster \
    --region ap-northeast-2 \
    --tasks eeb0a1e3dc3240b5ac2c538c88b3873b
```


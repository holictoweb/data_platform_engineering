
# doc

[공식 문서 ](https://docs.prefect.io/concepts/flows/#flow-runs)

### task_runners
- BaseTaskRunner
- ConcurrentTaskRunner
- SequentialTaskRunner

```bash
# server ( orion ) 시작 
prefect orion start


# queue 시작 
prefect work-queue start create "aicel_1"

# agent 실행 work-queue 지정하여 실행 
prefect agent start --work-queue "aicel_1"


# flow 등록 실행 ()
python 파일명

# deployments (스케쥴 작업을 돌리기 위해 필요 )

```

# 1. flow / flow-run


# 2. deployment

```py
from demo import pipeline
from prefect.deployments import Deployment

deployment = Deployment.build_from_flow(
    flow=pipeline,
    name="Python Deployment Example",
)

if __name__ == "__main__":
    deployment.apply()
```



# connect 

```py



```
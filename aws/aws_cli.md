# cloudwatch



```bash
# log group 생성
aws logs create-log-group --log-group-name /ecs/aicel_kg_builder

# log streams 생성 
aws logs create-log-stream --log-group-name /ecs/aicel_kg_builder --log-stream-name ecs/aicel_kg_builder 
```


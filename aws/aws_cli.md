# cloudwatch



```bash
# log group 생성
aws logs create-log-group --log-group-name /ecs/aicel_kg_builder

# log streams 생성 
aws logs create-log-stream --log-group-name /ecs/aicel_kg_builder --log-stream-name ecs/aicel_kg_builder 
```


# ecr 관련
# https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html 


```
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com

```
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



# s3

```bash
# bucket create
aws s3 mb s3://bucket-name
# bucket delete
aws s3 rb s3://bucket-name

# s3 path to local path
aws s3 cp s3://aicel-nlp/oss-packages/dev/confluentinc-kafka-connect-jdbc-10.5.0.zip .
```
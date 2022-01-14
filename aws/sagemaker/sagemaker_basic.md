
# sagemaker boto3
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html
- 기본적인 boto3 clinet 생성

```py
import boto3

region = 'ap-northeast-2'
client = boto3.client('sagemaker', region_name = region)

account = '445772965351'
image = "{}.dkr.ecr.{}.amazonaws.com/pytorch-extending:latest".format(account, region)
# role = get_execution_role()
role = 'arn:aws:iam::445772965351:role/fngo-sagemaker-execution-role'
```



- metric 정보 저장
https://docs.aws.amazon.com/sagemaker/latest/dg/training-metrics.html
```python
estimator =
                Estimator(image_name=ImageName,
                role='SageMakerRole', 
                instance_count=1,
                instance_type='ml.c4.xlarge',
                k=10,
                sagemaker_session=sagemaker_session,
                metric_definitions=[
                   {'Name': 'train:error', 'Regex': 'Train_error=(.*?);'},
                   {'Name': 'validation:error', 'Regex': 'Valid_error=(.*?);'}
                ]
            )
```

```python
import sagemaker
from sagemaker.pytorch.model import PyTorchModel

region = sagemaker.Session(boto3.session.Session()).boto_region_name
print("AWS Region: {}".format(region))

role = 'arn:aws:iam::324235234:role/fngo-sagemaker-execution-role'
print("RoleArn: {}".format(role))
```

# sagemaker job 조회 

- [sagemaker sdk](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.list_endpoints)

```
```





# endpoint

## endpoint 생성



- [boto3 endpoint 생성 유형 ](https://docs.aws.amazon.com/sagemaker/latest/dg/neo-deployment-hosting-services-boto3.html)

```python

import boto3
client = boto3.client('sagemaker', region_name = 'ap-northeast-2')

# create sagemaker model
create_model_api_response = client.create_model(
                                    ModelName='my-sagemaker-model',
                                    PrimaryContainer={
                                        'Image': <insert the ECR Image URI>,
                                        'ModelDataUrl': 's3://path/to/model/artifact/model.tar.gz',
                                        'Environment': {}
                                    },
                                    ExecutionRoleArn='ARN for AmazonSageMaker-ExecutionRole'
                            )

print ("create_model API response", create_model_api_response)

# create sagemaker endpoint config
create_endpoint_config_api_response = client.create_endpoint_config(
                                            EndpointConfigName='sagemaker-neomxnet-endpoint-configuration',
                                            ProductionVariants=[
                                                {
                                                    'VariantName': <provide your variant name>,
                                                    'ModelName': 'my-sagemaker-model',
                                                    'InitialInstanceCount': 1,
                                                    'InstanceType': <provide your instance type here>
                                                },
                                            ]
                                       )

print ("create_endpoint_config API response", create_endpoint_config_api_response)

# create sagemaker endpoint
create_endpoint_api_response = client.create_endpoint(
                                    EndpointName='provide your endpoint name',
                                    EndpointConfigName=<insert your endpoint config name>,
                                )

print ("create_endpoint API response", create_endpoint_api_response)     
```



##  endpoint 상태 확인

```python
res_ner = client.describe_endpoint(
            EndpointName=NER_BATCH_ENDPOINT
        )

```




# Sagemaker Endpoint



- serverless inference
- https://aws.amazon.com/ko/about-aws/whats-new/2021/12/amazon-sagemaker-serverless-inference/
  








- metric 정보 저장
https://docs.aws.amazon.com/sagemaker/latest/dg/training-metrics.html
```
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

import boto3
import json
import os

def invoke_model(var_list):
    """
    Invokes a SageMaker model specified in env settings and returns a float
    representing the stds from the mean.
    """
    client = boto3.client('sagemaker-runtime')

    endpoint_name = os.environ['SAGEMAKER_MODEL_NAME']
    content_type = 'application/json'
    request_body = {'Input': var_list}
    data = json.loads(json.dumps(request_body))
    payload = json.dumps(data)

    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType=content_type,
        Body=payload
    )

    result = json.loads(response['Body'].read())
    return result

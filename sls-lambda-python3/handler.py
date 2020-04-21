import json

def hello(event, context):
    body = {
        "message": "Hello World AWS Serverless V1"
    }

    print('Debug: ', body)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

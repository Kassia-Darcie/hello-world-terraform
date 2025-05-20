import json


def lambda_handler(event, context):
    return response(200, "Hellow Terraform!")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
    }

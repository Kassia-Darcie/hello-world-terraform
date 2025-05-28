import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME")

if TABLE_NAME:
    table = dynamodb.Table(TABLE_NAME)
else:
    table = None

def lambda_handler(event, context):
    try:
        user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
        response = table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
            & Key("SK").begins_with("ITEM#")
        )
        items = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps({"tasks": items})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

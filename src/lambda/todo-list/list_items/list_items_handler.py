import os
import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])
        user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
        response = table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
            & Key("SK").begins_with("ITEM#")
        )
        items = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps({"tasks": items})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

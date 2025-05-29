import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])

def lambda_handler(event, context):
    try:
        user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]

        date = event.get("queryStringParameters", {}).get("date")

        if not date:
            return {"statusCode": 400, "body": json.dumps({"error": "Date is required"})}

        response = table.query(
            KeyConditionExpression=Key("PK").eq(f"LIST#{generate_list_id(date)}") &
            Key("SK").begins_with("ITEM#")
        )
        items = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps({"tasks": items})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    

def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
    }


def generate_list_id(date):
    return date.replace("-", "")
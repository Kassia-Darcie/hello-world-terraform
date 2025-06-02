import json
import os
import uuid
from datetime import date



import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError



dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        if not body:
            return response(400, {"message": "Corpo da requisição não pode estar vazio."})
        
        user_id = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {}).get("sub")

        nome = body.get("nome")
        data = body.get("data")

        if not nome or not data:
            return response(400, {"message": "nome e data são obrigatórios"})

        new_item = {
            "PK": f"LIST#{generate_list_id(data)}",
            "SK": f"ITEM#{uuid.uuid4()}",
            "user_id": user_id,
            "nome": nome,
            "data": data,
            "status": "TODO",
        }

        table.put_item(
            Item=new_item,
            ConditionExpression=Attr("PK").not_exists() & Attr("SK").not_exists(),
        )

        return response(
            200, {"message": "Item adicionado com sucesso.", "item": new_item}
        )

    except ClientError as e:
        return response(
            500, {"message": "Erro no servidor: " + e.response["Error"]["Message"]}
        )
    except Exception as ex:
        return response(500, {"message": "Erro interno: " + str(ex)})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
    }


def generate_list_id(date):
    return date.replace("-", "")
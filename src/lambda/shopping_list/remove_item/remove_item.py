import json
import os

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    try:
        item_id = event.get("item_id")
        list_id = event.get("list_id")

        if not item_id or not list_id:
            return response(400, {"message": "item_id e list_id são obrigatórios."})

        delete_response = table.delete_item(
            Key={"PK": f"LIST#{list_id}", "SK": f"ITEM#{item_id}"},
            ReturnValues="ALL_OLD",
        )

        deleted_item = delete_response.get("Attributes")

        if deleted_item is not None:
            return response(
                200, {"message": "Item deletado com sucesso", "item": deleted_item}
            )
        else:
            return response(404, {"message": "Item não encontrado."})

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

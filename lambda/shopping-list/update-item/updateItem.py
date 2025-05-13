import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    TABLE_NAME = "shopping-list"
    table = dynamodb.Table(TABLE_NAME)

    try:
        item_id = event.get("item_id")
        list_id = event.get("list_id")

        if not item_id or not list_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "item_id and list_id são obrigatórios"}),
            }

        nome = event.get("nome")
        data = event.get("data")
        status = event.get("status")

        if not (nome or data or status):
            return response(
                400, {"message": "Nenhum campo para atualizar foi fornecido."}
            )

        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"

        item = table.get_item(Key={"PK": pk, "SK": sk})

        if "Item" not in item:
            return response(404, {"message": "Item não encontrado."})

        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        update_clauses = []

        if nome is not None:
            update_clauses.append("#N = :n")
            expression_attribute_names["#N"] = "nome"
            expression_attribute_values[":n"] = nome

        if data is not None:
            update_clauses.append("#D = :d")
            expression_attribute_names["#D"] = "data"
            expression_attribute_values[":d"] = data

        if status is not None:
            if status not in ["TODO", "DONE"]:
                return response(400, {"message": "Status deve ser 'TODO' ou 'DONE'."})
            update_clauses.append("#S = :s")
            expression_attribute_names["#S"] = "status"
            expression_attribute_values[":s"] = status

        update_expression += ", ".join(update_clauses)

        # Atualizar o item
        updated_item = table.update_item(
            Key={"PK": pk, "SK": sk},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )

        item = updated_item.get("Attributes", {})
        return response(200, {"updatedItem": item})

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

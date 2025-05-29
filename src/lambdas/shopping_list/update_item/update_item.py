import json
import os
from datetime import date

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])


def lambda_handler(event, context):
    try:
        path_params = event.get("pathParameters", {})
        item_id = path_params.get("id_do_item")

        if not item_id:
            return response(400, {"message": "id_do_item é obrigatório no path."})

        body = json.loads(event.get("body", "{}"))
        if not body:
            return response(400, {"message": "Corpo da requisição não pode estar vazio."})

        nome = body.get("nome")
        data = body.get("data")
        status = body.get("status")

        if not (nome or data or status):
            return response(400, {"message": "nome, data ou status são obrigatórios"})

        # Encontrar o item existente testando datas próximas
        sk = f"ITEM#{item_id}"
        existing_item, current_pk = find_existing_item(sk)
        
        if not existing_item:
            return response(404, {"message": "Item não encontrado."})

        current_data = existing_item["data"]
        
        # Se a data está sendo atualizada e é diferente da atual
        if data and data != current_data:
            new_list_id = generate_list_id(data)
            new_pk = f"LIST#{new_list_id}"
            
            # Delete old item
            table.delete_item(Key={"PK": current_pk, "SK": sk})
            
            # Create new item 
            new_item = {
                "PK": new_pk,
                "SK": sk,
                "nome": nome if nome is not None else existing_item["nome"],
                "data": data,
                "status": status if status is not None else existing_item["status"],
            }
            
            table.put_item(Item=new_item)
            return response(200, {"message": "Item atualizado com sucesso.", "item": new_item})

        # Se a data não está mudando, apenas atualiza outros campos
        pk = current_pk
        
        # Build update expression
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        update_clauses = []

        if nome is not None:
            update_clauses.append("#N = :n")
            expression_attribute_names["#N"] = "nome"
            expression_attribute_values[":n"] = nome

        if status is not None:
            if status not in ["TODO", "DONE"]:
                return response(400, {"message": "Status deve ser 'TODO' ou 'DONE'."})
            update_clauses.append("#S = :s")
            expression_attribute_names["#S"] = "status"
            expression_attribute_values[":s"] = status

        update_expression += ", ".join(update_clauses)

        # Update the item
        updated_item = table.update_item(
            Key={"PK": pk, "SK": sk},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )

        return response(200, {"message": "Item atualizado com sucesso.", "item": updated_item.get("Attributes", {})})

    except ClientError as e:
        return response(500, {"message": "Erro no servidor: " + e.response["Error"]["Message"]})
    except Exception as ex:
        return response(500, {"message": "Erro interno: " + str(ex)})


def find_existing_item(sk):
    """
    Tenta encontrar o item existente testando datas próximas à data atual.
    """
    today = date.today()
    
    # Testa hoje e alguns dias antes/depois
    for days_offset in range(-7, 8):  
        test_date = today.replace(day=today.day)
        try:
            if days_offset != 0:
                import datetime
                test_date = today + datetime.timedelta(days=days_offset)
        except:
            continue
            
        test_date_str = test_date.strftime("%Y-%m-%d")
        list_id = generate_list_id(test_date_str)
        pk = f"LIST#{list_id}"
        
        try:
            item = table.get_item(Key={"PK": pk, "SK": sk})
            if "Item" in item:
                return item["Item"], pk
        except ClientError:
            continue
    
    return None, None


def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
    }


def generate_list_id(date):
    return date.replace("-", "")
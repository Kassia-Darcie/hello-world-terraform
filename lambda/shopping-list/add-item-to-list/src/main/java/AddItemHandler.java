import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.ConditionalCheckFailedException;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class AddItemHandler implements RequestHandler<Map<String, Object>, Map<String, Object>> {
    private static final String TABLE_NAME = "shopping-list";
    private final DynamoDbClient dynamoDbClient = DynamoDbClient.create();


    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {
        try {
            String nome = (String) input.get("nome");
            String data = (String) input.get("data");

            if (nome == null || nome.isEmpty() || data == null || data.isEmpty()) {
                return errorResponse(400, "Nome e data são obrigatórios");
            }

            String pk = "LIST#" + data.replace("-", "");
            String itemId = UUID.randomUUID().toString();
            String sk = "ITEM#" + itemId;

            Map<String, AttributeValue> item = new HashMap<>();
            item.put("PK", AttributeValue.builder().s(pk).build());
            item.put("SK", AttributeValue.builder().s(sk).build());
            item.put("nome", AttributeValue.builder().s(nome).build());
            item.put("data", AttributeValue.builder().s(data).build());
            item.put("status", AttributeValue.builder().s(status).build());

            PutItemRequest putItemRequest = PutItemRequest.builder()
                    .tableName(TABLE_NAME)
                    .item(item)
                    .conditionExpression("attribute_not_exists(PK) and attribute_not_exists(SK)")
                    .build();

            dynamoDbClient.putItem(putItemRequest);

            Map<String, Object> responseData = new HashMap<>();
            responseData.put("PK", pk);
            responseData.put("SK", sk);
            responseData.put("nome", nome);
            responseData.put("data", data);
            responseData.put("status", "TODO");

            Map<String, Object> response = new HashMap<>();
            response.put("statusCode", 201);
            response.put("body", responseData);
            return response;


        } catch (ConditionalCheckFailedException e) {
            return errorResponse(409, "O item já existe");
        } catch (Exception e) {
            return Map.of("statusCode", 500, "erro", "Erro interno: " + e.getMessage());
        }

    }

    private Map<String, Object> errorResponse(int statusCode, String errorMessage) {
        Map<String, Object> response = new HashMap<>();
        response.put("statusCode", statusCode);
        response.put("body", Map.of("error", errorMessage));
        return response;
    }
}



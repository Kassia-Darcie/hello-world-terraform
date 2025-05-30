resource "aws_apigatewayv2_api" "api" {
  name          = "lnsi-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id           = aws_apigatewayv2_api.api.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name             = "cognito-authorizer"
  jwt_configuration {
    audience = [var.user_pool_client_id]
    issuer   = "https://cognito-idp.${var.region}.amazonaws.com/${var.user_pool_id}"
  }
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /hello"

  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "stage" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "prod"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      caller         = "$context.identity.caller"
      user           = "$context.identity.user"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })
  }
}

resource "aws_cloudwatch_log_group" "api_gw_logs" {
  name              = "/aws/apigateway/lnsi-gateway"
  retention_in_days = 14
}

resource "aws_lambda_permission" "api_gw_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*/hello"
}

resource "aws_apigatewayv2_route" "list_items_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /lista-tarefa"

  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.list_items_integration.id}"
}

resource "aws_apigatewayv2_integration" "list_items_integration" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.list_items_function_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_lambda_permission" "list_items_api_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.list_items_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*/lista-tarefa"
}

resource "aws_apigatewayv2_integration" "add_item_integration" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.add_item_function_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "add_item_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /lista-tarefa"

  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.add_item_integration.id}"
}

resource "aws_lambda_permission" "add_item_api_permission" {
  statement_id  = "AllowAPIGatewayInvokeAddItem"
  action        = "lambda:InvokeFunction"
  function_name = var.add_item_function_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_apigatewayv2_integration" "update_item_integration" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.update_item_function_arn
  integration_method     = "PUT"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "update_item_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "PUT /lista-tarefa/{id_do_item}"

  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.update_item_integration.id}"
}

resource "aws_lambda_permission" "update_item_api_permission" {
  statement_id  = "AllowAPIGatewayInvokeUpdateItem"
  action        = "lambda:InvokeFunction"
  function_name = var.update_item_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*/lista-tarefa/*"
}

output "api_url" {
  value = aws_apigatewayv2_stage.stage.invoke_url
}
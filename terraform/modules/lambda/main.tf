
resource "aws_lambda_function" "hello_terraform" {
  function_name = var.function_name
  runtime       = var.lambda_runtime
  role          = aws_iam_role.iam_role_for_lambda.arn
  filename      = var.lambda_filename
  handler       = var.lambda_handler
  timeout       = 15
}



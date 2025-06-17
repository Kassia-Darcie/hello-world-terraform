output "lambda_function_arn" {
  value = aws_lambda_function.lambda_hello.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_hello.function_name
}


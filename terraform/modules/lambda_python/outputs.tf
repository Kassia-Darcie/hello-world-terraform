output "lambda_function_arn" {
  value = aws_lambda_function.lambda_py.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_py.function_name
}


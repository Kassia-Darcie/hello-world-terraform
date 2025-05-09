output "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB criada."
  value       = aws_dynamodb_table.shopping-list.name
}

output "dynamodb_table_arn" {
  description = "ARN da tabela DynamoDB criada."
  value       = aws_dynamodb_table.shopping-list.arn
}
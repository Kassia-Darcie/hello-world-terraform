output "cognito_user_pool" {
  value = aws_cognito_user_pool.user_pool.id
}

output "cognito_user_pool_client" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}

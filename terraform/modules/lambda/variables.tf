variable "iam_role_name" {}
variable "function_name" {}
variable "lambda_runtime" {}
variable "lambda_filename" {}
variable "lambda_handler" {}
variable "dynamodb_arn" {
  type = string
}

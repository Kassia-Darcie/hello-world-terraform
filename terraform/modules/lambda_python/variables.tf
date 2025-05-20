variable "iam_role_name" {}
variable "function_name" {}
variable "lambda_runtime" {}
variable "lambda_handler" {}
variable "dynamodb_arn" {
  type = string
}
variable "source_dir" {
  type = string
}

variable "environment_variables" {
    type = map(string)
}

variable "region" {}
variable "lambda_function_arn" {}
variable "user_pool_id" {}
variable "user_pool_client_id" {}
variable "lambda_function_name" {
  type = string
}
variable "list_items_function_arn" {
  type = string
}

variable "list_items_function_name" {
  type = string
}

variable "add_item_function_arn" {
  description = "ARN da função Lambda que adiciona um item (add_item.py)"
  type        = string
}

variable "add_item_function_name" {
  description = "Nome da função Lambda que adiciona um item (add_item.py)"
  type        = string
}


provider "aws" {
  region = var.region
}

module "hello-terraform" {
  source         = "./modules/lambda"
  function_name  = "hello_terraform"
  lambda_runtime = "python3.13"
  lambda_handler = "hello_terraform.lambda_handler"
  iam_role_name  = "hello_role"
  source_dir     = "/../src/lambda/hello_world"
}

module "dynamodb-shopping-list" {
  source            = "./modules/dynamodb"
  dynamo_table_name = "shopping-list"
  hash_key_name     = "PK"
  range_key_name    = "SK"
}

module "add-item" {
  source         = "./modules/lambda_python"
  function_name  = "add_item"
  lambda_runtime = "python3.13"
  lambda_handler = "add_item.lambda_handler"
  iam_role_name  = "add_item_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "add_item"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}

module "update-item" {
  source         = "./modules/lambda_python"
  function_name  = "update_item"
  lambda_runtime = "python3.13"
  lambda_handler = "updateItem.lambda_handler"
  iam_role_name  = "update_item_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "update_item"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}

module "remove-item" {
  source         = "./modules/lambda_python"
  function_name  = "remove_item"
  lambda_runtime = "python3.13"
  lambda_handler = "removeItem.lambda_handler"
  iam_role_name  = "remove_item_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "remove_item"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}

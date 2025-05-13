provider "aws" {
  region = var.region
}

module "hello-terraform" {
  source          = "../../modules/lambda"
  function_name   = "hello_terraform"
  lambda_runtime  = "java21"
  lambda_filename = "../../../lambda/hello-world/target/hello-world-1.0-SNAPSHOT.jar"
  lambda_handler  = "com.estudo.HelloWorldHandler"
  iam_role_name   = "hello_role"
  dynamodb_arn    = module.dynamodb-shopping-list.dynamodb_table_arn
}

module "dynamodb-shopping-list" {
  source            = "../../modules/dynamodb"
  dynamo_table_name = "shopping-list"
  hash_key_name     = "PK"
  range_key_name    = "SK"
}

module "add-item-to-list" {
  source          = "../../modules/lambda"
  function_name   = "add_item_to_list"
  lambda_runtime  = "java21"
  lambda_filename = "../../../lambda/shopping-list/add-item-to-list/target/add-item-to-list-1.0-SNAPSHOT.jar"
  lambda_handler  = "AddItemHandler::handleRequest"
  iam_role_name   = "add_item_to_list_role"
  dynamodb_arn    = module.dynamodb-shopping-list.dynamodb_table_arn
}

module "update-item" {
  source         = "../../modules/lambda_python"
  function_name  = "update_item"
  lambda_runtime = "python3.13"
  lambda_handler = "updateItem.lambda_handler"
  iam_role_name  = "update_item_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "../../../lambda/shopping-list/update-item"
}

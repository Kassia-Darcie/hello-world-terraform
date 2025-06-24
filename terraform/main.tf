
module "cognito" {
  source = "./modules/cognito"
}

module "hello-terraform" {
  source         = "./modules/lambda"
  function_name  = "hello_terraform"
  lambda_runtime = "python3.13"
  lambda_handler = "hello_terraform.lambda_handler"
  iam_role_name  = "hello_role"
  source_dir     = "../src/lambdas/hello_world"
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
  source_dir     = "${path.root}/../src/lambdas/shopping_list/add_item"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}


module "update-item" {
  source         = "./modules/lambda_python"
  function_name  = "update_item"
  lambda_runtime = "python3.13"
  lambda_handler = "update_item.lambda_handler"
  iam_role_name  = "update_item_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "${path.root}/../src/lambdas/shopping_list/update_item"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}


module "remove-item" {
  source         = "./modules/lambda_python"
  function_name  = "remove_item"
  lambda_runtime = "python3.13"
  lambda_handler = "remove_item.lambda_handler"
  iam_role_name  = "remove_item_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "${path.root}/../src/lambdas/shopping_list/remove_item"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}


module "list-items" {
  source         = "./modules/lambda_python"
  function_name  = "list_items"
  lambda_runtime = "python3.13"
  lambda_handler = "list_items_handler.lambda_handler"
  iam_role_name  = "list_items_role"
  dynamodb_arn   = module.dynamodb-shopping-list.dynamodb_table_arn
  source_dir     = "${path.root}/../src/lambdas/shopping_list/list_items"
  environment_variables = {
    DYNAMODB_TABLE_NAME = "shopping-list"
  }
}

module "api_gateway" {
  source                    = "./modules/apigateway"
  lambda_function_arn       = module.hello-terraform.lambda_function_arn
  lambda_function_name      = module.hello-terraform.lambda_function_name
  list_items_function_arn   = module.list-items.lambda_function_arn
  list_items_function_name  = module.list-items.lambda_function_name
  add_item_function_arn     = module.add-item.lambda_function_arn
  add_item_function_name    = module.add-item.lambda_function_name
  update_item_function_arn  = module.update-item.lambda_function_arn
  update_item_function_name = module.update-item.lambda_function_name
  user_pool_id              = module.cognito.cognito_user_pool
  user_pool_client_id       = module.cognito.cognito_user_pool_client
  region                    = var.region
}

output "cognito_user_pool_id" {
  value = module.cognito.cognito_user_pool
}

output "cognito_user_pool_client_id" {
  value = module.cognito.cognito_user_pool_client
}

output "api_gateway_url" {
  value = module.api_gateway.api_url
}

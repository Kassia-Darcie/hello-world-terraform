resource "aws_dynamodb_table" "shopping-list" {
  name         = var.dynamo_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.hash_key_name
  range_key    = var.range_key_name

  attribute {
    name = var.hash_key_name
    type = "S"
  }

  attribute {
    name = var.range_key_name
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name            = "user_id"
    hash_key        = "user_id"
    range_key       = "PK"
    projection_type = "ALL"

  }
}


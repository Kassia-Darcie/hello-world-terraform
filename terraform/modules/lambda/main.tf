provider "aws" {
  region = var.region
}

resource "aws_lambda_function" "hello_terraform" {
  function_name = "hello_terraform"
  runtime       = var.lambda_runtime
  role          = aws_iam_role.iam_role_for_lambda.arn
  filename      = var.lambda_filename
  handler       = var.lambda_handler
  timeout       = 60
}

resource "aws_iam_role" "iam_role_for_lambda" {
  name               = "lambda-invoke-role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
}
EOF
}

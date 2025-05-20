resource "aws_iam_role" "iam_role_for_lambda" {
  name               = "${var.function_name}-iam-role"
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

resource "aws_iam_policy" "lambda_dynamodb_access_policy" {
  name        = "${var.function_name}-dynamodb-policy"
  description = "Permite que a Lambda acesse a tabela DynamoDB específica"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          # Ajuste as ações conforme necessário para sua Lambda
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem"
        ]
        # Referencia o ARN da tabela DynamoDB criada pelo Terraform
        # Substitua "minha_tabela_dados" pelo nome do seu recurso aws_dynamodb_table
        Resource = var.dynamodb_arn
      },
      {
        Effect = "Allow"
        Action = [
          # Permissão para descrever a tabela, útil para alguns SDKs
          "dynamodb:DescribeTable",
        ]
        # Permissão para descrever a tabela (pode ser no nível da tabela ou * na região)
        Resource = var.dynamodb_arn # Ou "arn:aws:dynamodb:*:*:table/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attach" {
  role       = aws_iam_role.iam_role_for_lambda.name
  policy_arn = aws_iam_policy.lambda_dynamodb_access_policy.arn
}

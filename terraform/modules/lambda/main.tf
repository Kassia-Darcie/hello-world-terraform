
resource "aws_lambda_function" "lambda_hello" {
  function_name    = var.function_name
  runtime          = var.lambda_runtime
  role             = aws_iam_role.iam_role_for_lambda.arn
  filename         = data.archive_file.lambda_zip.output_path
  handler          = var.lambda_handler
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 15
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.root}/${var.source_dir}"
  output_path = "${path.module}/zip/${var.function_name}.zip"

}



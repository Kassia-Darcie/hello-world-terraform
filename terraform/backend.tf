terraform {
  backend "s3" {
    bucket         = "kassiadarcie-sa-east-1-terraform-statefile"
    key            = "env:/dev/hello-world-terraform"
    region         = "sa-east-1"
    dynamodb_table = "kassiadarcie-sa-east-1-terraform-lock"
  }
}

variable "region" {
  default = "us-east-1"
}

variable "lambda_runtime" {
  default = "java21"
}

variable "lambda_filename" {
  default = "../lambda/hello-world/target/hello-world-1.0-SNAPSHOT.jar"
}

variable "lambda_handler" {
  default = "com.estudo.HelloWorldHandler"
}

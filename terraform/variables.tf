variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "environment" {
  description = "Deployment Environment"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "enable_glue_processing" {
  description = "Enable AWS Glue Crawler and ETL Job when the AWS account permits them"
  type        = bool
  default     = false
}

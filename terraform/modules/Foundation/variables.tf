variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}


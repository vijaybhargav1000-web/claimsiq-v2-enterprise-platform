variable "vpc_id" {
  type = string
}

variable "environment" {
  type = string
}

variable "ssh_cidr" {
  type    = string
  default = "157.50.107.186/32"
}
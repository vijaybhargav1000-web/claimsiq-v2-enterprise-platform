variable "environment" {
  type = string
}

variable "glue_database_name" {
  type = string
}

variable "bronze_bucket" {
  type = string
}

variable "silver_bucket" {
  type = string
}

variable "enable_glue_processing" {
  type    = bool
  default = false
}

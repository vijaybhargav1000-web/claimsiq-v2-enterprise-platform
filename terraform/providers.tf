provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ClaimsIQ-v2"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "Vijay Bhargav"
    }
  }
}
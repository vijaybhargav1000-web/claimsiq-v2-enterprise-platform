resource "aws_s3_bucket" "terraform_state" {
  bucket = "${var.project_name}-${var.environment}-terraform-state"

  tags = {
    Name = "Terraform State Bucket"
  }
}

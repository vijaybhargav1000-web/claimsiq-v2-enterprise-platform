resource "aws_nat_gateway" "main" {
  availability_mode = "regional"
  connectivity_type = "public"
  vpc_id            = var.vpc_id

  tags = {
    Name        = "claimsiq-v2-nat"
    Environment = var.environment
  }
}
resource "aws_lb" "main" {

  name = "claimsiq-${var.environment}-alb"

  internal = false

  load_balancer_type = "application"

  security_groups = [
    var.security_group_id
  ]

  subnets = var.public_subnet_ids

  enable_deletion_protection = false

  tags = {
    Name        = "claimsiq-${var.environment}-alb"
    Environment = var.environment
  }
}
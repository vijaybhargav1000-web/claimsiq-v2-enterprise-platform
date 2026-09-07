resource "aws_lb" "main" {

 name = "claimsiq-v2-alb"

  internal = false

  load_balancer_type = "application"

  security_groups = [
    var.security_group_id
  ]

  subnets = var.public_subnet_ids

  enable_deletion_protection = false

  tags = {
   name = "claimsiq-v2-alb"
    Environment = var.environment
  }
}
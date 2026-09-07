resource "aws_lb_target_group" "main" {

  name = "claimsiq-v2-tg"

  port     = 80
  protocol = "HTTP"

  vpc_id = var.vpc_id

  target_type = "instance"

  health_check {

    enabled = true

    path = "/"

    protocol = "HTTP"

    matcher = "200"

    interval = 30

    timeout = 5

    healthy_threshold = 5

    unhealthy_threshold = 2
  }

  tags = {
    Name        = "claimsiq-v2-tg"
    Environment = var.environment
  }
}
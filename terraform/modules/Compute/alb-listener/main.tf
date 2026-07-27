resource "aws_lb_listener" "http" {

  load_balancer_arn = var.load_balancer_arn

  port     = 80
  protocol = "HTTP"

  default_action {

    type = "forward"

    target_group_arn = var.target_group_arn

  }

}
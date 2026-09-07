resource "aws_lb_listener" "http" {

  load_balancer_arn = var.load_balancer_arn

  port     = 80
  protocol = "HTTP"

  default_action {

    type = "forward"

    target_group_arn = var.target_group_arn

    forward {

      target_group {
        arn    = var.target_group_arn
        weight = 1
      }

      stickiness {
        enabled  = false
        duration = 3600
      }
    }
  }
}
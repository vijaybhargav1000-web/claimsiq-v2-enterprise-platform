resource "aws_autoscaling_group" "main" {

  name = "claimsiq-${var.environment}-asg"

  desired_capacity = 2
  min_size         = 2
  max_size         = 4

  vpc_zone_identifier = var.private_subnet_ids

  target_group_arns = [
    var.target_group_arn
  ]

  launch_template {

    id      = var.launch_template_id
    version = "$Latest"

  }

  health_check_type         = "ELB"
  health_check_grace_period = 300

  force_delete = true

  tag {

    key                 = "Name"
    value               = "claimsiq-${var.environment}-ec2"
    propagate_at_launch = true

  }

}
resource "aws_autoscaling_group" "main" {

  name = "claimsiq-v2-asg"

  desired_capacity = 1
  min_size         = 1
  max_size         = 2

  vpc_zone_identifier = var.private_subnet_ids

  target_group_arns = [
    var.target_group_arn
  ]

  launch_template {
    id      = var.launch_template_id
    version = "2"
  }

  health_check_type         = "ELB"
  health_check_grace_period = 300

  force_delete            = true
  default_instance_warmup = 300
  enabled_metrics = [
    "WarmPoolPendingCapacity",
    "GroupTerminatingRetainedCapacity",
    "WarmPoolTerminatingRetainedCapacity",
    "WarmPoolDesiredCapacity",
    "GroupMaxSize",
    "GroupPendingInstances",
    "GroupTotalInstances",
    "WarmPoolMinSize",
    "GroupMinSize",
    "GroupStandbyCapacity",
    "GroupDesiredCapacity",
    "GroupAndWarmPoolTotalCapacity",
    "GroupInServiceCapacity",
    "GroupTerminatingRetainedInstances",
    "GroupStandbyInstances",
    "WarmPoolPendingRetainedCapacity",
    "GroupAndWarmPoolDesiredCapacity",
    "GroupTerminatingInstances",
    "WarmPoolWarmedCapacity",
    "GroupPendingCapacity",
    "WarmPoolTotalCapacity",
    "GroupTotalCapacity",
    "GroupInServiceInstances",
    "GroupTerminatingCapacity",
    "WarmPoolTerminatingCapacity"
  ]
  instance_maintenance_policy {
    min_healthy_percentage = 100
    max_healthy_percentage = 110
  }

  tag {
    key                 = "Name"
    value               = "ClaimsIQ-V2-ASG"
    propagate_at_launch = true
  }
}
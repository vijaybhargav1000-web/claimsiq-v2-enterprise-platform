resource "aws_cloudwatch_log_group" "main" {
  name              = "/claimsiq/${var.environment}"
  retention_in_days = 30
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "claimsiq-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6

        properties = {
          title  = "ClaimsIQ ASG CPU Utilization"
          region = "ap-south-1"
          stat   = "Average"
          period = 300
          view   = "timeSeries"

          metrics = [
            ["AWS/EC2", "CPUUtilization", "AutoScalingGroupName", "claimsiq-v2-asg"]
          ]
        }
      }
    ]
  })
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "claimsiq-${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  dimensions = {
    AutoScalingGroupName = "claimsiq-v2-asg"
  }
}

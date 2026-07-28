resource "aws_cloudwatch_log_group" "main" {

  name              = "/claimsiq/${var.environment}"
  retention_in_days = 30

}

resource "aws_cloudwatch_dashboard" "main" {

  dashboard_name = "claimsiq-${var.environment}"

  dashboard_body = jsonencode({
    widgets = []
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

}
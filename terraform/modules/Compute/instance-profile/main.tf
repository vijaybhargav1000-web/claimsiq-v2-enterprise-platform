resource "aws_iam_instance_profile" "ec2_profile" {
  name = "claimsiq-${var.environment}-instance-profile"
  role = var.ec2_role_name
}
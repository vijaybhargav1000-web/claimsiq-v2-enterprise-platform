resource "aws_iam_instance_profile" "ec2_profile" {
  name = "InstanceRole"
  role = var.ec2_role_name
}
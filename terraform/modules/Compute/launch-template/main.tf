data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_launch_template" "main" {
  name        = "claimsiq-v2-lt"
  description = "V2-SSM-Enabled-Production"
  image_id    = "ami-0a449ca57355f3459"

  instance_type = "t3.micro"

  key_name = "claimsiq-v2-key"

  vpc_security_group_ids = [
    var.security_group_id
  ]

  iam_instance_profile {
    name = var.instance_profile_name
  }

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name        = "claimsiq-v2-ec2"
      Environment = var.environment
    }
  }
}
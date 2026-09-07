resource "aws_security_group" "ec2_sg" {
  name        = "claimsiq-v2-ec2-sg"
  description = "Security group for ClaimsIQ EC2 application server "
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    cidr_blocks     = ["157.50.107.186/32"]
    prefix_list_ids = ["pl-0fa83cebf909345ca"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "claimsiq-v2-ec2-sg"
    Environment = var.environment
  }
}
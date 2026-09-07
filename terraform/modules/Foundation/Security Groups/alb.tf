resource "aws_security_group" "alb_sg" {
  name        = "claimsiq-v2-alb-sg"
  description = "Allows HTTP access to ClaimsIQ ALB"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

 tags = {
  Name        = "claimsiq-v2-alb-sg"
  Environment = var.environment

  }
}
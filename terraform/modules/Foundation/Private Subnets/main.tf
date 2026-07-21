resource "aws_subnet" "private_1" {
  vpc_id                  = var.vpc_id
  cidr_block              = "10.0.11.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "claimsiq-${var.environment}-private-subnet-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id                  = var.vpc_id
  cidr_block              = "10.0.12.0/24"
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = false

  tags = {
    Name = "claimsiq-${var.environment}-private-subnet-2"
  }
}
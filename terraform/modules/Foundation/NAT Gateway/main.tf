resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name        = "claimsiq-${var.environment}-nat-eip"
    Environment = var.environment
  }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = var.public_subnet_1_id

  tags = {
    Name        = "claimsiq-${var.environment}-nat-gateway"
    Environment = var.environment
  }

  depends_on = [aws_eip.nat]
}
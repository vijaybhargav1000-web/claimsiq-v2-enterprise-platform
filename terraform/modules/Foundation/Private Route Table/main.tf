resource "aws_route_table" "private" {
  vpc_id = var.vpc_id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = var.nat_gateway_id
  }

  tags = {
    Name        = "claimsiq-${var.environment}-private-rt"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = var.private_subnet_1_id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = var.private_subnet_2_id
  route_table_id = aws_route_table.private.id
}
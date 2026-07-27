resource "aws_s3_bucket" "bronze" {

  bucket = "claimsiq-${var.environment}-bronze"

  tags = {
    Name = "Bronze"
    Environment = var.environment
  }

}

resource "aws_s3_bucket" "silver" {

  bucket = "claimsiq-${var.environment}-silver"

  tags = {
    Name = "Silver"
    Environment = var.environment
  }

}

resource "aws_s3_bucket" "gold" {

  bucket = "claimsiq-${var.environment}-gold"

  tags = {
    Name = "Gold"
    Environment = var.environment
  }

}

resource "aws_s3_bucket" "scripts" {

  bucket = "claimsiq-${var.environment}-scripts"

  tags = {
    Name = "Scripts"
    Environment = var.environment
  }

}

resource "aws_s3_bucket_versioning" "bronze" {

  bucket = aws_s3_bucket.bronze.id

  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_s3_bucket_versioning" "silver" {

  bucket = aws_s3_bucket.silver.id

  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_s3_bucket_versioning" "gold" {

  bucket = aws_s3_bucket.gold.id

  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_s3_bucket_versioning" "scripts" {

  bucket = aws_s3_bucket.scripts.id

  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_s3_bucket_public_access_block" "bronze" {

  bucket = aws_s3_bucket.bronze.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true

}
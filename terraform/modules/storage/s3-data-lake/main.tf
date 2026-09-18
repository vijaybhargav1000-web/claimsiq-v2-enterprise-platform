resource "aws_s3_bucket" "bronze" {

  bucket = "claimsiq-v2-dev-bronze-2026"

  tags = {
    Name        = "Bronze"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "silver" {

  bucket = "claimsiq-v2-dev-silver-2026"

  tags = {
    Name        = "Silver"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "gold" {

  bucket = "claimsiq-v2-dev-gold-2026"

  tags = {
    Name        = "Gold"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "scripts" {

  bucket = "claimsiq-v2-dev-scripts-2026"

  tags = {
    Name        = "Scripts"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "athena_results" {

  bucket = "claimsiq-v2-dev-athena-results-2026"

  tags = {
    Name        = "Athena Results"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "ai_results" {

  bucket = "claimsiq-v2-dev-ai-results-2026"

  tags = {
    Name        = "AI Results"
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

resource "aws_s3_bucket_versioning" "ai_results" {

  bucket = aws_s3_bucket.ai_results.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "ai_results" {

  bucket = aws_s3_bucket.ai_results.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_public_access_block" "silver" {

  bucket = aws_s3_bucket.silver.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "gold" {

  bucket = aws_s3_bucket.gold.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "scripts" {

  bucket = aws_s3_bucket.scripts.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "athena_results" {

  bucket = aws_s3_bucket.athena_results.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "athena_results" {

  bucket = aws_s3_bucket.athena_results.id

  versioning_configuration {
    status = "Enabled"
  }
}

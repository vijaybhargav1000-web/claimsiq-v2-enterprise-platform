output "bronze_bucket" {
  value = aws_s3_bucket.bronze.bucket
}

output "silver_bucket" {
  value = aws_s3_bucket.silver.bucket
}

output "gold_bucket" {
  value = aws_s3_bucket.gold.bucket
}

output "scripts_bucket" {
  value = aws_s3_bucket.scripts.bucket
}

resource "aws_s3_bucket" "athena_results" {
  bucket = "claimsiq-${var.environment}-athena-results"
}

output "athena_results_bucket" {
  value = aws_s3_bucket.athena_results.bucket
}
resource "aws_iam_role" "glue_role" {

  name = "claimsiq-${var.environment}-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "glue.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })

}

resource "aws_iam_role_policy_attachment" "glue_service_role" {

  role = aws_iam_role.glue_role.name

  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"

}

resource "aws_glue_crawler" "bronze" {

  name = "claimsiq-${var.environment}-bronze-crawler"

  role = aws_iam_role.glue_role.arn

  database_name = var.glue_database_name

  s3_target {
    path = "s3://${var.bronze_bucket}/"
  }

}
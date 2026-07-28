
resource "aws_glue_job" "bronze_to_silver" {

  name     = "claimsiq-${var.environment}-bronze-to-silver"
  role_arn = var.glue_role_arn

  glue_version = "4.0"

  command {
    name            = "glueetl"
    script_location = "s3://${var.scripts_bucket}/bronze_to_silver.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language" = "python"
  }

  max_retries      = 0
  timeout          = 30
  number_of_workers = 2
  worker_type      = "G.1X"
}
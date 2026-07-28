resource "aws_athena_workgroup" "main" {

  name = "claimsiq-${var.environment}"

  configuration {

    enforce_workgroup_configuration = true

    result_configuration {

      output_location = "s3://${var.results_bucket}/athena-results/"
    }
  }
}
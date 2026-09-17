output "glue_job_name" {
  value = var.enable_glue_processing ? aws_glue_job.bronze_to_silver[0].name : null
}

output "crawler_name" {
  value = var.enable_glue_processing ? aws_glue_crawler.bronze[0].name : null
}

output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}

output "crawler_name" {
  value = aws_glue_crawler.bronze.name
}

output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}
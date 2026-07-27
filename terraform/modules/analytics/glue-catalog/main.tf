resource "aws_glue_catalog_database" "main" {

  name = "claimsiq_${var.environment}_catalog"

  description = "Glue Catalog Database for ClaimsIQ"

}
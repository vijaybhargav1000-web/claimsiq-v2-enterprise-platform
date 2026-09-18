module "foundation" {
  source = "./modules/Foundation"

  project_name = "claimsiq-v2"
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
}

module "public_subnets" {
  source = "./modules/Foundation/Public Subnets"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}

module "private_subnets" {
  source = "./modules/Foundation/Private Subnets"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}

module "internet_gateway" {
  source = "./modules/Foundation/Internet Gateway"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}
module "route_tables" {
  source = "./modules/Foundation/Route Tables"

  vpc_id              = module.foundation.vpc_id
  internet_gateway_id = module.internet_gateway.internet_gateway_id
  environment         = var.environment

  public_subnet_1_id = module.public_subnets.public_subnet_1_id
  public_subnet_2_id = module.public_subnets.public_subnet_2_id
}

module "nat_gateway" {
  source = "./modules/Foundation/NAT Gateway"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}
module "private_route_table" {
  source = "./modules/Foundation/Private Route Table"

  vpc_id              = module.foundation.vpc_id
  nat_gateway_id      = module.nat_gateway.nat_gateway_id
  private_subnet_1_id = module.private_subnets.private_subnet_1_id
  private_subnet_2_id = module.private_subnets.private_subnet_2_id
  environment         = var.environment
}

module "security_groups" {
  source = "./modules/Foundation/Security Groups"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}

module "iam_role" {
  source = "./modules/Compute/IAM Role"

  environment = var.environment
}

module "instance_profile" {
  source = "./modules/Compute/instance-profile"

  ec2_role_name = module.iam_role.ec2_role_name
  environment   = var.environment
}
module "launch_template" {

  source = "./modules/Compute/launch-template"

  environment = var.environment

  security_group_id = module.security_groups.ec2_security_group_id

  instance_profile_name = module.instance_profile.instance_profile_name
}

module "target_group" {

  source = "./modules/Compute/target-group"

  vpc_id = module.foundation.vpc_id

  environment = var.environment
}

module "application_load_balancer" {

  source = "./modules/Compute/application-load-balancer"

  environment = var.environment

  security_group_id = module.security_groups.alb_security_group_id

  public_subnet_ids = [
    module.public_subnets.public_subnet_1_id,
    module.public_subnets.public_subnet_2_id
  ]
}

module "alb_listener" {

  source = "./modules/Compute/alb-listener"

  load_balancer_arn = module.application_load_balancer.alb_arn

  target_group_arn = module.target_group.target_group_arn

}

module "auto_scaling_group" {

  source = "./modules/Compute/auto-scaling-group"

  environment = var.environment

  launch_template_id = module.launch_template.launch_template_id
  launch_template_version = module.launch_template.launch_template_latest_version

  target_group_arn = module.target_group.target_group_arn

  private_subnet_ids = [
    module.private_subnets.private_subnet_1_id,
    module.private_subnets.private_subnet_2_id
  ]

}

module "s3_data_lake" {

  source = "./modules/storage/s3-data-lake"

  environment = var.environment

}

module "glue_catalog" {

  source = "./modules/analytics/glue-catalog"

  environment = var.environment

}

module "glue_crawler" {

  source = "./modules/analytics/glue-crawler"

  environment            = var.environment
  glue_database_name     = module.glue_catalog.glue_database_name
  bronze_bucket          = module.s3_data_lake.bronze_bucket
  silver_bucket          = module.s3_data_lake.silver_bucket
  enable_glue_processing = var.enable_glue_processing

}

module "glue_etl_job" {

  source = "./modules/analytics/glue-etl-job"

  environment            = var.environment
  glue_role_arn          = module.glue_crawler.glue_role_arn
  scripts_bucket         = module.s3_data_lake.scripts_bucket
  enable_glue_processing = var.enable_glue_processing

}
module "athena" {

  source = "./modules/analytics/athena"

  environment    = var.environment
  results_bucket = module.s3_data_lake.athena_results_bucket
}
module "cloudwatch" {

  source = "./modules/monitoring/cloudwatch"

  environment = var.environment

}

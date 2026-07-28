module "foundation" {
  source = "./modules/foundation"

  project_name = "claimsiq-v2"
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
}

module "public_subnets" {
  source = "./modules/foundation/Public Subnets"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}

module "private_subnets" {
  source = "./modules/foundation/Private Subnets"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}

module "internet_gateway" {
  source = "./modules/foundation/Internet Gateway"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}
module "route_tables" {
  source = "./modules/foundation/Route Tables"

  vpc_id              = module.foundation.vpc_id
  internet_gateway_id = module.internet_gateway.internet_gateway_id
  environment         = var.environment

  public_subnet_1_id = module.public_subnets.public_subnet_1_id
  public_subnet_2_id = module.public_subnets.public_subnet_2_id
}

module "nat_gateway" {
  source = "./modules/foundation/NAT Gateway"

  public_subnet_1_id = module.public_subnets.public_subnet_1_id
  environment        = var.environment
}
module "private_route_table" {
  source = "./modules/foundation/Private Route Table"

  vpc_id              = module.foundation.vpc_id
  nat_gateway_id      = module.nat_gateway.nat_gateway_id
  private_subnet_1_id = module.private_subnets.private_subnet_1_id
  private_subnet_2_id = module.private_subnets.private_subnet_2_id
  environment         = var.environment
}

module "security_groups" {
  source = "./modules/foundation/Security Groups"

  vpc_id      = module.foundation.vpc_id
  environment = var.environment
}

module "iam_role" {
  source = "./modules/compute/IAM Role"

  environment = var.environment
}

module "instance_profile" {
  source = "./modules/compute/instance-profile"

  ec2_role_name = module.iam_role.ec2_role_name
  environment   = var.environment
}
module "launch_template" {

  source = "./modules/compute/launch-template"

  environment = var.environment

  security_group_id = module.security_groups.ec2_security_group_id

  instance_profile_name = module.instance_profile.instance_profile_name
}

module "target_group" {

  source = "./modules/compute/target-group"

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

  target_group_arn = module.target_group.target_group_arn

  private_subnet_ids = [
    module.private_subnets.private_subnet_1_id,
    module.private_subnets.private_subnet_2_id
  ]

}

module "s3_data_lake" {

  source = "./modules/Storage/s3-data-lake"

  environment = var.environment

}

module "glue_catalog" {

  source = "./modules/Analytics/glue-catalog"

  environment = var.environment

}

module "glue_crawler" {

  source = "./modules/Analytics/glue-crawler"

  environment = var.environment

  glue_database_name = module.glue_catalog.glue_database_name

  bronze_bucket = module.s3_data_lake.bronze_bucket

}

module "glue_etl_job" {

  source = "./modules/Analytics/glue-etl-job"

  environment = var.environment

  glue_role_arn = module.glue_crawler.glue_role_arn

  scripts_bucket = module.s3_data_lake.scripts_bucket
}
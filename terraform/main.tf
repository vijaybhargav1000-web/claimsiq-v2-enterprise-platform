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
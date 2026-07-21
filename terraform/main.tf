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
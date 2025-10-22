module "global_scale" {
  source = "./modules/global"
  node_count = 5
  enable_autoscaling = true
  cloud_targets = ["azure","aws","oracle","gcp"]
}

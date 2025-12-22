provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

module "network" {
  source      = "../../modules/network"
  environment = "staging"
  zone        = var.zone
}

module "kubernetes" {
  source        = "../../modules/kubernetes"
  environment   = "staging"
  zone          = var.zone
  network_id    = module.network.network_id
  subnet_id     = module.network.subnet_id
  cluster_sa_id = var.cluster_sa_id
  node_sa_id    = var.node_sa_id
  kms_key_id    = var.kms_key_id
}

module "storage" {
  source      = "../../modules/storage"
  environment = "staging"
  service_account_id = var.service_account_id
}

module "monitoring" {
  source                   = "../../modules/monitoring"
  environment              = "staging"
  notification_channel_id  = var.notification_channel_id
}

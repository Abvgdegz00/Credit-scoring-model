resource "yandex_storage_bucket" "models_bucket" {
  name                  = "credit-scoring-${var.environment}-models"
  service_account_id    = var.service_account_id
  force_destroy         = true
  acl                   = "private"
}

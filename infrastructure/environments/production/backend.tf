terraform {
  backend "s3" {
    bucket = "credit-scoring-terraform-state"
    key    = "production/terraform.tfstate"
    region = "ru-central1"
  }
}

terraform {
  backend "s3" {
    bucket = "credit-scoring-terraform-state"
    key    = "staging/terraform.tfstate"
    region = "ru-central1"
  }
}

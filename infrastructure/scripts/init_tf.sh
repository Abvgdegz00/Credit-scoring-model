#!/bin/bash
terraform init -backend-config="bucket=credit-scoring-terraform-state" \
               -backend-config="key=$1/terraform.tfstate" \
               -backend-config="region=ru-central1"
terraform plan -var="environment=$1" -out=tfplan
terraform apply "tfplan"

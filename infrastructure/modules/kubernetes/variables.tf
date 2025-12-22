variable "environment" { type = string }
variable "zone" { type = string }
variable "network_id" { type = string }
variable "subnet_id" { type = string }
variable "cluster_sa_id" { type = string }
variable "node_sa_id" { type = string }
variable "kms_key_id" { type = string }
variable "security_group_id" {
  type        = string
  description = "ID security group для master и node groups"
}

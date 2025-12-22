output "k8s_cluster_id" { value = yandex_kubernetes_cluster.credit_scoring.id }
output "k8s_cluster_endpoint" { value = yandex_kubernetes_cluster.credit_scoring.endpoint }
output "kubeconfig" {
  value = yandex_kubernetes_cluster.credit_scoring.kubeconfig.0.raw_config
  sensitive = true
}
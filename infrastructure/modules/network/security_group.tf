resource "yandex_vpc_security_group" "k8s_sg" {
  name       = "k8s-${var.environment}-sg"
  network_id = var.network_id

  # Kubernetes API
  ingress {
    protocol       = "TCP"
    port           = 6443
    v4_cidr_blocks = ["0.0.0.0/0"]
    description    = "Kubernetes API"
  }

  # HTTPS
  ingress {
    protocol       = "TCP"
    port           = 443
    v4_cidr_blocks = ["0.0.0.0/0"]
    description    = "HTTPS"
  }

  # Kubelet
  ingress {
    protocol       = "TCP"
    port           = 10250
    v4_cidr_blocks = ["0.0.0.0/0"]
    description    = "Kubelet API"
  }

  # NodePort диапазон
  ingress {
    protocol       = "TCP"
    port           = 30000
    port_to        = 32767
    v4_cidr_blocks = ["0.0.0.0/0"]
    description    = "NodePort services"
  }

  # Все исходящие соединения
  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}

output "k8s_sg_id" {
  value = yandex_vpc_security_group.k8s_sg.id
}

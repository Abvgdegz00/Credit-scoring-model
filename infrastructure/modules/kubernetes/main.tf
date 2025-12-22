resource "yandex_kubernetes_cluster" "credit_scoring" {
  name       = "credit-scoring-${var.environment}"
  network_id = var.network_id

  master {
    version   = "1.24"
    public_ip = true

    master_location {
      zone      = var.zone
      subnet_id = var.subnet_id
    }

    service_account_id      = var.cluster_sa_id
    node_service_account_id = var.node_sa_id

    kms_provider {
      key_id = var.kms_key_id
    }

    network {
      security_group_ids = [var.security_group_id]
    }
  }
}

resource "yandex_kubernetes_node_group" "cpu_nodes" {
  cluster_id = yandex_kubernetes_cluster.credit_scoring.id
  name       = "cpu-nodes-${var.environment}"

  instance_template {
    platform_id = "standard-v2"

    resources {
      memory = 8
      cores  = 4
    }

    boot_disk {
      type = "network-ssd"
      size = 64
    }

    scheduling_policy {
      preemptible = var.environment != "production"
    }

    network {
      security_group_ids = [var.security_group_id]
    }
  }

  scale_policy {
    auto_scale {
      min     = 2
      max     = 10
      initial = 2
    }
  }
}

resource "yandex_kubernetes_node_group" "gpu_nodes" {
  cluster_id = yandex_kubernetes_cluster.credit_scoring.id
  name       = "gpu-nodes-${var.environment}"

  instance_template {
    platform_id = "gpu-1"

    resources {
      memory = 16
      cores  = 8
    }

    boot_disk {
      type = "network-ssd"
      size = 128
    }

    network {
      security_group_ids = [var.security_group_id]
    }

    # GPU labels
    labels = {
      "gpu"  = "true"
      "type" = "nvidia"
    }

    # GPU taint
    taint {
      key    = "gpu"
      value  = "true"
      effect = "NoSchedule"
    }
  }

  scale_policy {
    auto_scale {
      min     = 0
      max     = 5
      initial = 0
    }
  }
}

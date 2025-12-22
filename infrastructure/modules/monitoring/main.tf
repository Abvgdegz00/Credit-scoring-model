resource "yandex_monitoring_alert" "cpu_alert" {
  name        = "high-cpu-${var.environment}"
  description = "Alert if CPU > 80%"

  condition {
    comparison = ">"
    metric     = "compute_instance_cpu_utilization"
    threshold  = 80
    period     = 300
  }

  notification_channels = [var.notification_channel_id]
}

resource "yandex_monitoring_alert" "memory_alert" {
  name        = "high-mem-${var.environment}"
  description = "Alert if memory > 80%"

  condition {
    comparison = ">"
    metric     = "compute_instance_memory_utilization"
    threshold  = 80
    period     = 300
  }

  notification_channels = [var.notification_channel_id]
}

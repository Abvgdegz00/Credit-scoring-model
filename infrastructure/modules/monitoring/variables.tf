variable "environment" {
  type = string
  description = "Environment name (staging/production)"
}

variable "notification_channel_id" {
  type = string
  description = "ID notification channel for alerts"
}

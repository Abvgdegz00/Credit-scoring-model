resource "yandex_vpc_network" "network" {
  name = "credit-scoring-${var.environment}-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "credit-scoring-${var.environment}-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.2.0.0/16"]
}

terraform {
  required_version = ">= 0.13"
  required_providers {
    rabbitmq = {
      source = "cyrilgdn/rabbitmq"
    }
  }
}

variable "url" {}
variable "username" {}
variable "password" {}

provider "rabbitmq" {
  endpoint = var.url
  username = var.username
  password = var.password
}

resource "rabbitmq_exchange" "entity1" {
  name  = "entity1"
  vhost = "/"

  settings {
    type        = "fanout"
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_exchange" "entity2" {
  name  = "entity2"
  vhost = "/"

  settings {
    type        = "fanout"
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_exchange" "entity3" {
  name  = "entity3"
  vhost = "/"

  settings {
    type        = "fanout"
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_exchange" "entity4" {
  name  = "entity4"
  vhost = "/"

  settings {
    type        = "fanout"
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_queue" "service1_entity3" {
  name  = "service1.entity3"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}
resource "rabbitmq_queue" "service1_entity4" {
  name  = "service1.entity4"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}
resource "rabbitmq_queue" "service2_entity2" {
  name  = "service2.entity2"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}
resource "rabbitmq_queue" "service4_entity1" {
  name  = "service4.entity1"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}

resource "rabbitmq_queue" "service1_backfill_entity3" {
  name  = "service1.backfill.entity3"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}
resource "rabbitmq_queue" "service1_backfill_entity4" {
  name  = "service1.backfill.entity4"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}
resource "rabbitmq_queue" "service2_backfill_entity2" {
  name  = "service2.backfill.entity2"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}
resource "rabbitmq_queue" "service4_backfill_entity1" {
  name  = "service4.backfill.entity1"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = true
  }
}

resource "rabbitmq_binding" "service1_entity3_from_entity3" {
  source           = rabbitmq_exchange.entity3.name
  vhost            = "/"
  destination      = rabbitmq_queue.service1_entity3.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service1_entity4_from_entity4" {
  source           = rabbitmq_exchange.entity4.name
  vhost            = "/"
  destination      = rabbitmq_queue.service1_entity4.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service2_entity2_from_entity2" {
  source           = rabbitmq_exchange.entity2.name
  vhost            = "/"
  destination      = rabbitmq_queue.service2_entity2.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service4_entity1_from_entity1" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service4_entity1.name
  destination_type = "queue"
  routing_key      = ""
}

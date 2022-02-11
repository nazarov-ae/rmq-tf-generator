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

resource "rabbitmq_queue" "service2_entity1" {
  name  = "service2.entity1"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service4_entity2" {
  name  = "service4.entity2"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_queue" "service2_entity1_backfill" {
  name  = "service2.entity1.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service4_entity2_backfill" {
  name  = "service4.entity2.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_binding" "service2_entity1" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service2_entity1.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service4_entity2" {
  source           = rabbitmq_exchange.entity2.name
  vhost            = "/"
  destination      = rabbitmq_queue.service4_entity2.name
  destination_type = "queue"
  routing_key      = ""
}

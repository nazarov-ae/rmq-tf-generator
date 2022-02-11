resource "rabbitmq_exchange" "entity1" {
  name  = "entity1"
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
resource "rabbitmq_queue" "service3_entity1" {
  name  = "service3.entity1"
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
resource "rabbitmq_queue" "service3_entity1_backfill" {
  name  = "service3.entity1.backfill"
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
resource "rabbitmq_binding" "service3_entity1" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service3_entity1.name
  destination_type = "queue"
  routing_key      = ""
}

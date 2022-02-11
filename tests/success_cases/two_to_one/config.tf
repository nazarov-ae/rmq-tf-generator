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

resource "rabbitmq_queue" "service3_entity1" {
  name  = "service3.entity1"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service3_entity2" {
  name  = "service3.entity2"
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
resource "rabbitmq_queue" "service3_entity2_backfill" {
  name  = "service3.entity2.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_binding" "service3_entity1" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service3_entity1.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service3_entity2" {
  source           = rabbitmq_exchange.entity2.name
  vhost            = "/"
  destination      = rabbitmq_queue.service3_entity2.name
  destination_type = "queue"
  routing_key      = ""
}

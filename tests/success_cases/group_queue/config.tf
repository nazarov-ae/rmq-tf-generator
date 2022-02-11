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

resource "rabbitmq_queue" "service3_queue" {
  name  = "service3.queue"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_queue" "service3_queue_backfill" {
  name  = "service3.queue.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_binding" "service3_queue" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service3_queue.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service3_queue" {
  source           = rabbitmq_exchange.entity2.name
  vhost            = "/"
  destination      = rabbitmq_queue.service3_queue.name
  destination_type = "queue"
  routing_key      = ""
}

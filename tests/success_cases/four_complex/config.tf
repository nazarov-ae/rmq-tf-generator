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
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service1_entity4" {
  name  = "service1.entity4"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service2_entity2" {
  name  = "service2.entity2"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service4_entity1" {
  name  = "service4.entity1"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_queue" "service1_entity3_backfill" {
  name  = "service1.entity3.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service1_entity4_backfill" {
  name  = "service1.entity4.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service2_entity2_backfill" {
  name  = "service2.entity2.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service4_entity1_backfill" {
  name  = "service4.entity1.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_binding" "service1_entity3" {
  source           = rabbitmq_exchange.entity3.name
  vhost            = "/"
  destination      = rabbitmq_queue.service1_entity3.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service1_entity4" {
  source           = rabbitmq_exchange.entity4.name
  vhost            = "/"
  destination      = rabbitmq_queue.service1_entity4.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service2_entity2" {
  source           = rabbitmq_exchange.entity2.name
  vhost            = "/"
  destination      = rabbitmq_queue.service2_entity2.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service4_entity1" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service4_entity1.name
  destination_type = "queue"
  routing_key      = ""
}

resource "rabbitmq_user" "service1" {
  name     = "service1"
  password = ""
}
resource "rabbitmq_user" "service2" {
  name     = "service2"
  password = ""
}
resource "rabbitmq_user" "service3" {
  name     = "service3"
  password = ""
}
resource "rabbitmq_user" "service4" {
  name     = "service4"
  password = ""
}

resource "rabbitmq_permissions" "service1" {
  user  = rabbitmq_user.service1.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity1|entity2)"
    read     = "(service1\\.entity3|service1\\.entity3\\.backfill|service1\\.entity4|service1\\.entity4\\.backfill)"
  }
}
resource "rabbitmq_permissions" "service2" {
  user  = rabbitmq_user.service2.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity3)"
    read     = "(service2\\.entity2|service2\\.entity2\\.backfill)"
  }
}
resource "rabbitmq_permissions" "service3" {
  user  = rabbitmq_user.service3.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity4)"
    read     = ""
  }
}
resource "rabbitmq_permissions" "service4" {
  user  = rabbitmq_user.service4.name
  vhost = "/"

  permissions {
    configure = ""
    write    = ""
    read     = "(service4\\.entity1|service4\\.entity1\\.backfill)"
  }
}

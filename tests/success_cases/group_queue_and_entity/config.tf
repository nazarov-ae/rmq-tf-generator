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

resource "rabbitmq_queue" "service5_queue_group" {
  name  = "service5.queue_group"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service5_entity3" {
  name  = "service5.entity3"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_queue" "service5_queue_group_backfill" {
  name  = "service5.queue_group.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}
resource "rabbitmq_queue" "service5_entity3_backfill" {
  name  = "service5.entity3.backfill"
  vhost = "/"

  settings {
    durable     = true
    auto_delete = false
  }
}

resource "rabbitmq_binding" "service5_queue_group_entity1" {
  source           = rabbitmq_exchange.entity1.name
  vhost            = "/"
  destination      = rabbitmq_queue.service5_queue_group.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service5_queue_group_entity2" {
  source           = rabbitmq_exchange.entity2.name
  vhost            = "/"
  destination      = rabbitmq_queue.service5_queue_group.name
  destination_type = "queue"
  routing_key      = ""
}
resource "rabbitmq_binding" "service5_entity3" {
  source           = rabbitmq_exchange.entity3.name
  vhost            = "/"
  destination      = rabbitmq_queue.service5_entity3.name
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
resource "rabbitmq_user" "service5" {
  name     = "service5"
  password = ""
}

resource "rabbitmq_permissions" "service1" {
  user  = rabbitmq_user.service1.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity1)"
    read     = ""
  }
}
resource "rabbitmq_permissions" "service2" {
  user  = rabbitmq_user.service2.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity2)"
    read     = ""
  }
}
resource "rabbitmq_permissions" "service3" {
  user  = rabbitmq_user.service3.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity3)"
    read     = ""
  }
}
resource "rabbitmq_permissions" "service4" {
  user  = rabbitmq_user.service4.name
  vhost = "/"

  permissions {
    configure = ""
    write    = "(entity4)"
    read     = ""
  }
}
resource "rabbitmq_permissions" "service5" {
  user  = rabbitmq_user.service5.name
  vhost = "/"

  permissions {
    configure = ""
    write    = ""
    read     = "(service5\\.queue_group|service5\\.queue_group\\.backfill|service5\\.entity3|service5\\.entity3\\.backfill)"
  }
}

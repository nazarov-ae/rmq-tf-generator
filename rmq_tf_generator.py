import os
from os.path import (
    splitext, join, isdir, isfile, dirname, abspath, exists)
import re
import argparse

import jinja2


class MultipleProducerError(Exception):
    pass


class ProducerMissingError(Exception):
    pass


class ConfigBuilder:  # noqa: too-few-public-methods
    BASE_DIR = dirname(abspath(__file__))
    ENTITIES_TEMPLATE = r'.*\.json'
    RABBITMQ_TEMPLATE = 'rabbitmq.j2tf'
    USERS_FILE = 'users.json'

    def __init__(self, services_dir):
        self.services_dir = services_dir
        self.services = {}
        self._valid_produces = []

    def _collect_entities(self, entities_dir):
        return [
            splitext(entity)[0]
            for entity in os.listdir(entities_dir)
            if isfile(join(entities_dir, entity)) and
            re.match(self.ENTITIES_TEMPLATE, entity)
        ]

    def _collect_produces(self, service, service_dir):
        self.services[service]['produces'] = []
        produces_dir = join(service_dir, 'produces')
        if not exists(produces_dir) or not isdir(produces_dir):
            return
        self.services[service]['produces'] = self._collect_entities(
            produces_dir)

    def _collect_consumes_group_entity(self, service, entities_dir, entity):
        self.services[service]['consumes'].append({
            entity: self._collect_entities(entities_dir)
        })

    def _collect_consumes_entity(self, service, entity):
        if re.match(self.ENTITIES_TEMPLATE, entity):
            entity = splitext(entity)[0]
            self.services[service]['consumes'] += [entity]

    def _collect_consumes(self, service, service_dir):
        self.services[service]['consumes'] = []
        consumes_dir = join(service_dir, 'consumes')
        if not exists(consumes_dir) or not isdir(consumes_dir):
            return
        for entity in os.listdir(consumes_dir):
            entity_fs = join(consumes_dir, entity)
            if isdir(entity_fs):
                self._collect_consumes_group_entity(service, entity_fs, entity)
            if isfile(entity_fs):
                self._collect_consumes_entity(service, entity)

    def _collect_data(self):
        """
        Пример с обычными очередями.
        service1
        |- produces
           |- entity1
        service2
        |- consumes
           |- entity1

        'services': {
            'service1': {
                'produces': ['entity1'],
                'consumes': []
            },
            'service2': {
                'produces': [],
                'consumes': ['entity1']
            }
        }

        exchanges:      entity1
        queues:         service2.entity1
        bindings:
            entity1:    service2.entity1
        users:
            service1:
                write:  entity1
            service2:
                read:   service2.entity1

        Пример с группой очередей.
        service1
        |- produces
           |- entity1
        service2
        |- consumes
           |- group
              |- entity1

        'services': {
            'service1': {
                'produces': ['entity1'],
                'consumes': [],
            },
            'service2': {
                'produces': [],
                'consumes': [
                    {
                        'group': ['entity1']
                    }
                ]
            }
        }

        exchanges:      entity1
        queues:         service2.group
        bindings:
            entity1:    service2.group
        users:
            service1:
                write:  entity1
            service2:
                read:   service2.group
        """

        for service in os.listdir(self.services_dir):
            service_dir = join(self.services_dir, service)
            if not isdir(service_dir):
                continue
            self.services[service] = {}
            self._collect_produces(service, service_dir)
            self._collect_consumes(service, service_dir)

    def _validate_produces(self):
        self._valid_produces = []
        error_produces = []
        for rmq_entity in self.services.values():
            for producer in rmq_entity['produces']:
                if producer in self._valid_produces:
                    error_produces.append(producer)
                    continue
                self._valid_produces.append(producer)
        if error_produces:
            raise MultipleProducerError(error_produces)

    def _validate_consumes(self):
        error_consumes = []
        for rmq_entity in self.services.values():  # noqa: too-many-nested-blocks
            for consumer in rmq_entity['consumes']:
                if isinstance(consumer, dict):
                    for sub_consumes in consumer.values():
                        for sub_consume in sub_consumes:
                            if sub_consume not in self._valid_produces:
                                error_consumes.append(consumer)
                if isinstance(consumer, str):
                    if consumer not in self._valid_produces:
                        error_consumes.append(consumer)
        if error_consumes:
            raise ProducerMissingError(error_consumes)

    def _validate_data(self):
        self._validate_produces()
        self._validate_consumes()

    # TODO:
    #  * remove empty new line from result tf-file
    def _render(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.BASE_DIR),
            trim_blocks=True,
            lstrip_blocks=True)

        return env.get_template(self.RABBITMQ_TEMPLATE).render({
            'services': self.services,
        })

    def build(self):
        self._collect_data()
        self._validate_data()
        return self._render()


def main():
    parser = argparse.ArgumentParser('Generate terraform config for RabbitMQ')
    parser.add_argument(dest='services_dir',
                        help='Path to directory with services')
    args = parser.parse_args()

    config = ConfigBuilder(args.services_dir).build()
    print(config)


if __name__ == '__main__':
    main()

import os
from os.path import (
    split, splitext, join, isdir, isfile, dirname, abspath)
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

    def __init__(self, services_dir):
        self.services_dir = services_dir
        self.produces = []
        self.consumes = {}

    def _collect_produces(self, produces_dir):
        for entity in os.listdir(produces_dir):
            if not isfile(join(produces_dir, entity)):
                continue
            if re.match(self.ENTITIES_TEMPLATE, entity):
                self.produces.append(splitext(entity)[0])

    def _collect_group_consumes(self, service, entity_dir):
        entities = [
            splitext(entity)[0]
            for entity in os.listdir(entity_dir)
            if isfile(join(entity_dir, entity)) and
            re.match(self.ENTITIES_TEMPLATE, entity)
        ]
        self.consumes[f'{service}.{split(entity_dir)[1]}'] = entities

    def _collect_entity_consumes(self, service, entity):
        if re.match(self.ENTITIES_TEMPLATE, entity):
            entity = splitext(entity)[0]
            self.consumes[f'{service}.{entity}'] = [entity]

    def _collect_consumes(self, service, consume_dir):
        for entity in os.listdir(consume_dir):
            entity_dir = join(consume_dir, entity)
            if isdir(entity_dir):
                self._collect_group_consumes(service, entity_dir)
            if isfile(entity_dir):
                self._collect_entity_consumes(service, entity)

    def _collect_data(self):
        """
        Пример с плоскими очередями
        service1
        |- produces
           |- entity1
        service2
        |- consumes
           |- entity1

        'produces': ['e1']
        'consumes': {
          's2.e1': ['e1'],
        }

        exchanges: entity1
        queues:    service2.entity1
        bindings:  entity1>service2.entity1

        Пример с групповыми очередями
        service1
        |- produces
           |- entity1
           |- entity2
        service2
        |- consumes
           |- group
              |- entity1
              |- entity2

        'produces': ['entity1', 'entity2']
        'consumes': {
          'service2.group': ['entity1', 'entity2'],
        }

        exchanges: entity1, entity2
        queues:    service2.group
        bindings:  entity1>service2.group, entity2>service2.group
        """

        for service in os.listdir(self.services_dir):
            service_dir = join(self.services_dir, service)
            if not isdir(service_dir):
                continue
            for rmq_entity in os.listdir(service_dir):
                rmq_entity_dir = join(service_dir, rmq_entity)
                if not isdir(join(service_dir, rmq_entity)):
                    continue
                if rmq_entity == 'produces':
                    self._collect_produces(rmq_entity_dir)
                if rmq_entity == 'consumes':
                    self._collect_consumes(service, rmq_entity_dir)

    def _validate_data(self):
        produces = []
        error_produces = []
        for producer in self.produces:
            if producer in produces:
                error_produces.append(producer)
            produces.append(producer)
        if error_produces:
            raise MultipleProducerError(error_produces)

        error_consumes = []
        for entities in self.consumes.values():
            for entity in entities:
                if entity not in self.produces:
                    error_consumes.append(entity)
        if error_consumes:
            raise ProducerMissingError(error_consumes)

    def _render(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.BASE_DIR),
            trim_blocks=True,
            lstrip_blocks=True)

        env.filters.update({
            'fix_resource_name': lambda value: value.replace('.', '_')
        })

        return env.get_template(self.RABBITMQ_TEMPLATE).render({
            'produces': self.produces,
            'consumes': self.consumes,
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

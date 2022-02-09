import os
from os.path import (
    splitext, join, isdir, exists, dirname, abspath)
import re
import argparse

import jinja2


class MultipleProducerError(Exception):
    pass


class ProducerMissingError(Exception):
    pass


class LoopbackError(Exception):
    pass


class ConfigBuilder:  # noqa: too-few-public-methods
    BASE_DIR = dirname(abspath(__file__))
    ENTITIES_TEMPLATE = r'.*\.json'
    RABBITMQ_TEMPLATE = 'rabbitmq.j2'

    def __init__(self, services_dir):
        self.services_dir = services_dir
        self.produces = []
        self.consumes = []

    def _collect_data(self):
        for service_dir in os.listdir(self.services_dir):
            if not isdir(join(self.services_dir, service_dir)):
                continue
            rmq_entities = {
                'produces': [],
                'consumes': [],
            }
            for rmq_entity, entities in rmq_entities.items():
                dir_path = join(self.services_dir, service_dir, rmq_entity)
                if not exists(dir_path) or not isdir(dir_path):
                    continue
                for file in os.listdir(dir_path):
                    if isdir(file):
                        continue
                    if re.match(self.ENTITIES_TEMPLATE, file):
                        entities.append([splitext(file)[0], service_dir])
            for producer in rmq_entities['produces']:
                if producer in rmq_entities['consumes']:
                    raise LoopbackError(service_dir)
            self.produces += rmq_entities['produces']
            self.consumes += rmq_entities['consumes']

    def _validate_data(self):
        produces = []
        for entity, _ in self.produces:
            if entity in produces:
                raise MultipleProducerError(entity)
            produces.append(entity)

        consumes = []
        for entity, _ in self.consumes:
            if entity not in produces:
                raise ProducerMissingError(entity)
            consumes.append(entity)

    def _render(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.BASE_DIR),
            trim_blocks=True,
            lstrip_blocks=True)

        return env.get_template(self.RABBITMQ_TEMPLATE).render({
            'produces': self.produces,
            'consumes': self.consumes,
        })

    def build_config(self):
        self._collect_data()
        self._validate_data()
        return self._render()


def main():
    parser = argparse.ArgumentParser('Generate terraform config for RabbitMQ')
    parser.add_argument(dest='services_dir',
                        help='Path to directory with services')
    args = parser.parse_args()

    config = ConfigBuilder(args.services_dir).build_config()
    print(config)


if __name__ == '__main__':
    main()

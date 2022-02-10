import os
from os.path import (
    splitext, join, isdir, isfile, exists, dirname, abspath)
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
        self.consumes = []

    def _collect_data(self):
        '''
        s1
        |- produces
           |- e1
           |- e2
        s2
        |- consumes
           |- e1
           |- e2

        # 'produces': [
        #   ('e1', 's1')
        # ]
        # 'consumes': [
        #   ('e1', 's2')
        # ]
        'produces': ['e1', 's1']
        'consumes': {
          's2.e1': ['e1'],
          's2.e2': ['e2']
        }

        exchange    [P][e]                  e1
        exchange    [P][e]                  e2
        queue       [P][key]                s2.e1
        queue       [P][key]                s2.e2
        binding     [P][value]>[P][value]   e1>s2.e1
        binding     [P][value]>[P][value]   e2>s2.e2


        s1
        |- produces
           |- e1
           |- e2
        s2
        |- consumes
           |- d
              |- e1
              |- e2

        # 'produces': [
        #   ('e1', 's1')
        #   ('e2', 's1')
        # ]
        # 'consumes': [
        #     ('e1', 's2.d'),
        #     ('e2', 's2.d'),
        # ]
        'produces': ['e1', 's1']
        'consumes': {
          's2.d': ['e1', 'e2'],
        }

        exchange    [e]                     e1
        exchange    [e]                     e2
        queue       [P][key]                s2.2
        binding     [P][value]>[P][value]   e1>s2.d
        binding     [P][value]>[P][value]   e2>s2.d

        '''
        for service_dir in os.listdir(self.services_dir):
            if not isdir(join(self.services_dir, service_dir)):
                continue
            rmq_entities = {
                'produces': self.produces,
                'consumes': self.consumes,
            }
            for rmq_entity, entities in rmq_entities.items():
                dir_path = join(self.services_dir, service_dir, rmq_entity)
                if not exists(dir_path) or not isdir(dir_path):
                    continue
                for file in os.listdir(dir_path):
                    if not isfile(join(dir_path, file)):
                        continue
                    if re.match(self.ENTITIES_TEMPLATE, file):
                        entities.append([splitext(file)[0], service_dir])

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

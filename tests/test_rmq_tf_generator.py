import os
import json

import pytest

from rmq_tf_generator import (
    ConfigBuilder, MultipleProducerError, ProducerMissingError)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUCCESS_CASES_DIR = os.path.join(BASE_DIR, 'success_cases')
SERVICES_DIR = os.path.join(BASE_DIR, 'services')


@pytest.fixture
def fs_plus(fs):  # pylint:disable=invalid-name
    fs.add_real_file(
        os.path.join(ConfigBuilder.BASE_DIR, ConfigBuilder.RABBITMQ_TEMPLATE))
    fs.add_real_directory(SUCCESS_CASES_DIR)
    yield fs


def create_fake_fs(file_struct):
    def create_root_dir():
        os.makedirs(SERVICES_DIR)
        os.chdir(SERVICES_DIR)

    def create_struct(file_struct):
        for key, value in file_struct.items():
            if value is None:
                os.mknod(os.path.abspath(key))
                continue
            os.mkdir(key)
            os.chdir(key)
            create_struct(value)
            os.chdir('..')

    create_root_dir()
    create_struct(file_struct)


def get_success_cases_dirs():
    # for case_dir in os.listdir(SUCCESS_CASES_DIR):
    #     yield case_dir
    yield 'one_to_one'


@pytest.mark.parametrize('case_dir', get_success_cases_dirs())
def test_build_config(case_dir, fs_plus):  # noqa: redefined-outer-name
    fs_file = os.path.join(SUCCESS_CASES_DIR, case_dir, 'fs.json')
    with open(fs_file, encoding="utf-8") as file:
        file_struct = json.loads(file.read())
    config_file = os.path.join(SUCCESS_CASES_DIR, case_dir, 'config.tf')
    with open(config_file, encoding="utf-8") as file:
        excepted_config = file.read()

    create_fake_fs(file_struct)
    actual_config = ConfigBuilder(SERVICES_DIR).build()

    assert actual_config == excepted_config


def test_multiple_producer_error(fs_plus):  # noqa: redefined-outer-name
    create_fake_fs({
        'service1': {
            'produces': {
                'entity1.json': None,
            },
        },
        'service2': {
            'produces': {
                'entity1.json': None,
            },
        },
    })

    with pytest.raises(MultipleProducerError):
        ConfigBuilder(SERVICES_DIR).build()


@pytest.mark.parametrize('fs_struct', [
    {
        'service1': {
            'consumes': {
                'entity1.json': None,
            },
        },
    },
    {
        'service1': {
            'produces': {
                'entity1.json': None,
            },
        },
        'service2': {
            'consumes': {
                'entity2.json': None,
            },
        },
    },
])
def test_producer_missing_error(fs_struct, fs_plus):  # noqa: redefined-outer-name
    create_fake_fs(fs_struct)

    with pytest.raises(ProducerMissingError):
        ConfigBuilder(SERVICES_DIR).build()

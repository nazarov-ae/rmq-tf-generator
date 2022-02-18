import os
import json

import pytest

from rmq_tf_generator import (
    ConfigBuilder, MultipleProducerError, ProducerMissingError,
    ServiceAccountNotSetError, DuplicateServiceAccountError)


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

    def create_fs_struct(file_struct):
        for key, value in file_struct.items():
            if isinstance(value, dict):
                os.mkdir(key)
                os.chdir(key)
                create_fs_struct(value)
                os.chdir('..')
            if isinstance(value, str):
                with open(os.path.abspath(key), 'w', encoding='utf-8') as file:
                    file.write(value)

    create_root_dir()
    create_fs_struct(file_struct)


def get_success_cases_dirs():
    for case_dir in os.listdir(SUCCESS_CASES_DIR):
        yield case_dir
    # yield 'one_to_one'
    # yield 'group_queue'
    # yield 'double_two'


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


# @pytest.mark.parametrize('fs_struct, exception_match', [
#     (
#         {
#             'service1': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service1\"}"
#             },
#             'service2': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service2\"}"
#             },
#         },
#         ['entity1']
#     ),
#     (
#         {
#             'service1': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service1\"}"
#             },
#             'service2': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service2\"}"
#             },
#             'service3': {
#                 'produces': {
#                     'entity2.json': '',
#                 },
#                 "service.json": "{\"account\": \"service3\"}"
#             },
#             'service4': {
#                 'produces': {
#                     'entity2.json': '',
#                 },
#                 "service.json": "{\"account\": \"service4\"}"
#             },
#         },
#         ['entity1', 'entity2']
#     )
# ])
# def test_multiple_producer_error(fs_plus, fs_struct, exception_match):  # noqa: redefined-outer-name
#     create_fake_fs(fs_struct)
#
#     with pytest.raises(MultipleProducerError, match=str(exception_match)):
#         ConfigBuilder(SERVICES_DIR).build()


# @pytest.mark.parametrize('fs_struct, exception_match', [
#     (
#         {
#             'service1': {
#                 'consumes': {
#                     'entity1.json': '',
#                 },
#             },
#             "service.json": "{\"account\": \"service1\"}"
#         },
#         ['entity1']
#     ),
#     (
#         {
#             'service1': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service1\"}"
#             },
#             'service2': {
#                 'consumes': {
#                     'entity2.json': '',
#                 },
#                 "service.json": "{\"account\": \"service2\"}"
#             },
#         },
#         ['entity2']
#     ),
#     (
#         {
#             "service1": {
#                 "produces": {
#                     "entity1.json": '',
#                 },
#                 "service.json": "{\"account\": \"service1\"}"
#             },
#             "service2": {
#                 "consumes": {
#                     "queue": {
#                         "entity1.json": '',
#                         "entity2.json": '',
#                     }
#                 },
#                 "service.json": "{\"account\": \"service2\"}"
#             }
#         },
#         ['entity2']
#     )
# ])
# def test_producer_missing_error(fs_struct, fs_plus, exception_match):  # noqa: redefined-outer-name
#     create_fake_fs(fs_struct)
#
#     # TODO: match don't work?
#     with pytest.raises(ProducerMissingError, match=str(exception_match)):
#         ConfigBuilder(SERVICES_DIR).build()
#
#
# @pytest.mark.parametrize('fs_struct, exception_match', [
#     (
#         {
#             'service1': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 'service.json': '',
#             },
#             'service2': {
#                 'consumes': {
#                     'entity1.json': '',
#                 },
#                 'service.json': '',
#             },
#         },
#         ['service1', 'service2', ]
#     ),
# ])
# def test_service_account_not_set_error(fs_struct, fs_plus, exception_match):  # noqa: redefined-outer-name
#     create_fake_fs(fs_struct)
#
#     with pytest.raises(ServiceAccountNotSetError, match=str(exception_match)):
#         ConfigBuilder(SERVICES_DIR).build()
#
#
# @pytest.mark.parametrize('fs_struct, exception_match', [
#     (
#         {
#             'service1': {
#                 'produces': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service1\"}"
#             },
#             'service2': {
#                 'consumes': {
#                     'entity1.json': '',
#                 },
#                 "service.json": "{\"account\": \"service1\"}"
#             },
#         },
#         ['service1', 'service2', ]
#     ),
# ])
# def test_duplicate_service_account_error(fs_struct, fs_plus, exception_match):  # noqa: redefined-outer-name
#     create_fake_fs(fs_struct)
#
#     with pytest.raises(
#             DuplicateServiceAccountError, match=str(exception_match)):
#         ConfigBuilder(SERVICES_DIR).build()

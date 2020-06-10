""" Lockable plugin for pytest """
import random
import json
import socket
import os
from time import sleep
from contextlib import contextmanager
import tempfile
import pytest
from pydash import filter_, merge
from func_timeout import func_timeout, FunctionTimedOut
from filelock import Timeout, FileLock


def pytest_addoption(parser):
    """
    register argparse-style options and ini-style config values,
    called once at the beginning of a test run
    """
    parser.addoption("--allocation_hostname", default=socket.gethostname(), help="Allocation host")
    parser.addoption("--allocation_requirements", default=None, help="Resource requirements to be allocate")
    parser.addoption("--allocation_timeout", default=10, help="Allocation timeout")
    parser.addoption("--allocation_resource_list_file", default='resources.json', help="Resource to be allocate")
    parser.addoption("--allocation_lock_folder", default=tempfile.gettempdir(), help="allocation lock folder")


def read_resources_list(filename):
    """ Read resources json file """
    with open(filename) as json_file:
        data = json.load(json_file)
        assert isinstance(data, list), 'data is not an list'
    return data


def parse_requirements(requirements_str):
    """ Parse requirements """
    if not requirements_str:
        return dict()
    try:
        return json.loads(requirements_str)
    except json.decoder.JSONDecodeError:
        parts = requirements_str.split('&')
        if len(parts) == 0:
            raise ValueError('no requirements given')
        requirements = dict()
        for part in parts:
            try:
                part.index("=")
            except ValueError:
                continue
            key, value = part.split('=')
            requirements[key] = value
        return requirements


def _try_lock(candidate, lock_folder):
    """ Function that tries to lock given candidate resource """
    resource_id = candidate.get("id")
    try:
        lock_file = os.path.join(lock_folder, f"{resource_id}.lock")
        lockable = FileLock(lock_file)
        lockable.acquire(timeout=0)
        print(f'Allocated resource: {resource_id}')

        def release():
            print(f'Release resource: {resource_id}')
            lockable.release()
            try:
                os.remove(lock_file)
            except OSError:
                pass

        return candidate, release
    except Timeout:
        raise AssertionError('not success')


@contextmanager
def _lock_some(candidates, timeout_s, lock_folder, retry_interval):
    """ Contextmanager that lock some candidate that is free and release it finally """
    print(f'Total match local resources: {len(candidates)}, timeout: {timeout_s}')
    try:
        def doit(candidates_inner):
            while True:
                for candidate in candidates_inner:
                    try:
                        return _try_lock(candidate, lock_folder)
                    except AssertionError:
                        pass
                print('trying to lock after short period')
                sleep(retry_interval)

        resource, release = func_timeout(timeout_s, doit, args=(candidates,))
        print(f'resource {resource["id"]} allocated')
        yield resource
        release()
    except FunctionTimedOut:
        raise TimeoutError(f'Allocation timeout ({timeout_s}s)')


@contextmanager
def lock(requirements: dict, resource_list: list, timeout_s: int, lock_folder: str, retry_interval=1):
    """ Lock resource context """
    local_resources = filter_(resource_list, requirements)
    random.shuffle(local_resources)
    with _lock_some(local_resources, timeout_s, lock_folder, retry_interval) as resource:
        yield resource


def _get_requirements(requirements, hostname):
    """ Generate requirements"""
    print(f'hostname: {hostname}')
    return merge(dict(hostname=hostname, online=True), requirements)


@pytest.fixture(scope="session", params=[""])
def lockable_resource(request):
    """ pytest fixture that lock suitable resource and yield it """
    requirements = parse_requirements(request.config.getoption('allocation_requirements'))
    predicate = _get_requirements(requirements, request.config.getoption('allocation_hostname'))
    resource_list = read_resources_list(request.config.getoption('allocation_resource_list_file'))
    timeout_s = request.config.getoption('allocation_timeout')
    lock_folder = request.config.getoption('allocation_lock_folder')
    print(f"Use lock folder: {lock_folder}")
    print(f"Requirements: {json.dumps(predicate)}")
    print(f"Resource list: {json.dumps(resource_list)}")
    with lock(predicate, resource_list, timeout_s, lock_folder) as resource:
        yield resource

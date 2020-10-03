""" Lockable plugin for pytest """
import json
import socket
import tempfile
from contextlib import contextmanager
import pytest
from lockable import parse_requirements, get_requirements, read_resources_list, lock


def pytest_addoption(parser):
    """
    register argparse-style options and ini-style config values,
    called once at the beginning of a test run
    """
    group = parser.getgroup("lockable")
    group.addoption("--allocation_hostname", default=socket.gethostname(), help="Allocation host")
    group.addoption("--allocation_requirements", default=None, help="Resource requirements to be allocate")
    group.addoption("--allocation_timeout", default=10, help="Allocation timeout")
    group.addoption("--allocation_resource_list_file", default='resources.json', help="Available resorces list")
    group.addoption("--allocation_lock_folder", default=tempfile.gettempdir(), help="Allocation lockfiles folder")


@pytest.fixture(scope="session", autouse=True)
def lockable(pytestconfig, record_testsuite_property):
    """
    pytest fixture that yields function for allocate any resource
    .. code-block:: python
            def test_foo(lockable_allocate):
                with lockable({my: "resource}) as resource:
                    print(resource)
    """
    resource_list = read_resources_list(pytestconfig.getoption('allocation_resource_list_file'))
    timeout_s = pytestconfig.getoption('allocation_timeout')
    lock_folder = pytestconfig.getoption('allocation_lock_folder')

    @contextmanager
    def _lock(requirements, prefix='resource'):
        nonlocal resource_list, timeout_s, lock_folder
        requirements = parse_requirements(requirements)
        predicate = get_requirements(requirements, pytestconfig.getoption('allocation_hostname'))
        print(f"Use lock folder: {lock_folder}")
        print(f"Requirements: {json.dumps(predicate)}")
        print(f"Resource list: {json.dumps(resource_list)}")
        with lock(predicate, resource_list, timeout_s, lock_folder) as resource:
            for key, value in resource.items():
                record_testsuite_property(f'resource_{key}', value)
                if pytestconfig.pluginmanager.hasplugin('metadata'):
                    # pylint: disable=protected-access
                    pytestconfig._metadata[f'{prefix}_{key}'] = value
            yield resource

    yield _lock


@pytest.fixture(scope="session", autouse=True)
def lockable_resource(pytestconfig, lockable):  # pylint: disable=redefined-outer-name
    """
    pytest fixture that lock suitable resource and yield it
    .. code-block:: python
        def test_foo(lockable_resource):
            print(f'Testing with resource: {lockable_resource}')
    """
    requirements = pytestconfig.getoption('allocation_requirements')
    with lockable(requirements) as resource:
        yield resource

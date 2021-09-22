""" Lockable plugin for pytest """
import socket
import tempfile
import pytest
from lockable import Lockable


def pytest_addoption(parser):
    """
    register argparse-style options and ini-style config values,
    called once at the beginning of a test run
    """
    group = parser.getgroup("lockable")
    group.addoption("--allocation_hostname", default=socket.gethostname(), help="Allocation host")
    group.addoption("--allocation_requirements", default=None, help="Resource requirements to be allocate")
    group.addoption("--allocation_timeout", type=int, default=10, help="Allocation timeout")
    group.addoption("--allocation_resource_list_file", default='resources.json', help="Available resources list")
    group.addoption("--allocation_lock_folder", default=tempfile.gettempdir(), help="Allocation lockfiles folder")


@pytest.fixture(scope="session", autouse=True)
def lockable(pytestconfig):
    """
    pytest fixture that yields function for allocate any resource
    .. code-block:: python
            def test_foo(lockable):
                with lockable.auto_lock({my: "resource}) as allocation:
                    print(allocation.resource_info)
    """

    resource_list_file = pytestconfig.getoption('allocation_resource_list_file')
    lock_folder = pytestconfig.getoption('allocation_lock_folder')
    hostname = pytestconfig.getoption('allocation_hostname')

    _lockable = Lockable(hostname=hostname, resource_list_file=resource_list_file, lock_folder=lock_folder)
    yield _lockable


@pytest.fixture(scope="session", autouse=True)
def lockable_resource(pytestconfig, lockable):  # pylint: disable=redefined-outer-name
    """
    pytest fixture that lock suitable resource and yield it
    .. code-block:: python
        def test_foo(lockable_resource):
            print(f'Testing with resource: {lockable_resource}')
    """
    requirements = pytestconfig.getoption('allocation_requirements')
    timeout_s = pytestconfig.getoption('allocation_timeout')
    with lockable.auto_lock(requirements, timeout_s) as allocation:
        yield allocation.resource_info

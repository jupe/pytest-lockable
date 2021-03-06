""" Example test case for lockable_resource usage """
from time import sleep


def test_example(lockable_resource):
    """ Simple test """
    print(f'Testing with resource: {lockable_resource}')
    sleep(1)


def test_example1(lockable_resource):
    """ Simple test """
    print(f'Testing with resource: {lockable_resource}')
    sleep(1)


def test_example2(lockable_resource, lockable):
    """ Simple test """
    print(f'Testing with resource: {lockable_resource}')
    with lockable.auto_lock({}) as resource:
        print(f'Testing with resource#2: {resource}')
        sleep(1)

# pytest-lockable

[![CircleCI](https://circleci.com/gh/jupe/pytest-lockable/tree/master.svg?style=svg)](https://circleci.com/gh/jupe/pytest-lockable/tree/master)
[![PyPI version](https://badge.fury.io/py/pytest-lockable.svg)](https://badge.fury.io/py/pytest-lockable)
[![Coverage Status](https://coveralls.io/repos/github/jupe/pytest-lockable/badge.svg)](https://coveralls.io/github/jupe/pytest-lockable)

pytest plugin for lockable resources.

Replacement for Jenkins lockable -plugin.
Locking is implemented using `<resource-id>.pid` files and is released automatically.

Resources are automatically released when pytest ends.

Resources are described in json file as array of objects. Each object has some mandatory fields but can contains any other as well. Required fields are: `id`, `online`, `hostname`.

## Example `resources.json`

```
[
  {
    "id": "1234",
    "online": true,
    "hostname": "localhost",
    "os": "Android"
  }
]
```

`id` should be unique for each resources. `online` describes if resource are available for allocator. Set this `false`  if you don't want to allocate resource. `hostname` is used to select suitable resource by running host. 

Usage:
```
pytest --allocation_hostname localhost -s --allocation_requirements os=Android my_test
```


## installation

**Requires:** python 3.7<

```python
pip install pytest-lockable
```

`conftest.py`:

```
pytest_plugins = ("lockable.plugin",)
```

## integrations

pytest-lockable integrates pytest-metadata - when resource is 
reserved and [pytest-metadata](https://github.com/pytest-dev/pytest-metadata) plugin are in use metadata will 
be generated from resource json with  `resource_` -prefixes.
e.g. `resource_id=<id>`. 
Same dictionary are also recorded to testsuite property using
[record_testsuite_property](https://docs.pytest.org/en/stable/reference.html#record-testsuite-property) -method.

## Usage

Custom options:

```
--allocation_hostname=<hostname>, default=<os-hostname>  Allocation host
--allocation_requirements=<requirements>                 Resource requirements to be allocate
--allocation_timeout=<timeout>, default=10               Allocation timeout in seconds
--allocation_resource_list_file=<filename>, default=resources.json 
                                                         Available resorces list
--allocation_lock_folder=<folder>, default=<os-tmp-path> allocation lockfiles folder
```

*`<requirements>`* can be json-string or key-value pairs. requirements have to match available resources to make allocation possible. Key-value pairs example: `key=value&key2=value2` 

Example:

Use shared lockable resource
``` python
def test_example(lockable_resource):
    """ Simple test """
    print(f'Testing with resource: {lockable_resource}')
```

Allocate lockable resource during test with given requirements
``` python
def test_example(lockable):
    """ Simple test """
    with lockable.auto_lock({"my": "requirements"}) as resource:
        print(f'Testing with resource#: {resource}')
```

See [example test](example/test_example.py). Usage:
```
cd example
pytest --allocation_hostname localhost -s --allocation_lock_folder . .
```

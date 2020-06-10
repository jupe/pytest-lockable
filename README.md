# pytest-lockable
pytest plugin for lockable resources.

Replacement for Jenkins lockable -plugin.
Locking is implemented using `<resource.id>.lock` files.

## installation

**Requires:** python 3.7<

```python
pip install pytest-lockable
```

## Usage

Custom options:

```
--allocation_hostname=<hostname>, default=<os-hostname>  Allocation host
--allocation_requirements=<requirements>                 Resource requirements to be allocate
--allocation_timeout=<timeout>, default=10               Allocation timeout in seconds
--allocation_resource_list_file=<filename>, default=resources.json 
                                                         Resource to be allocate
--allocation_lock_folder=<folder>, default= os tmp path  allocation lock folder
```

Example:
```
cd example
pytest --allocation_hostname localhost -s --allocation_lock_folder .  .
```


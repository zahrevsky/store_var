# store_var

![Python](https://img.shields.io/badge/python-3.6-blue.svg)

Wrapper, that stores a list into a file on every list update. A band-aid 
solution for a small project, when database is an overkill.

```python
from store_var import stored

# Stores to file on first initializaiton
users = stored('users.pickle', [
    {'name': 'Gregory', 'age': 45},
    {'name': 'James', 'age': 37},
])

# Behaves as a list
print(f"There are {len(users)} users") # → There are 2 users

# On each change, storage file is updated
users.append({'name': 'Lisa', 'age': 38})

# ··· After restarting a REPL ···

users = stored('users.pickle')
print(users)
# → stored({'name': 'Gregory', 'age': 45}, {'name': 'James', 'age': 37}, {'name': 'Lisa', 'age': 38})
# Notice, that there are 3 users now
```

## Installation
```pip install store_var```

## Limitations
Wrappers for `reverse`, `sort`, `copy` and `deepcopy` are not implemented yet. 
Everything else works and is unit-tested.

Stores data using `pickle`.

Supports only a lists of picklable objects. Won't store a dict, or a list of lambdas.

## Examples
See tests.
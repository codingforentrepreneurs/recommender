# Celery Reference


## Running Celery

### Worker-only

```bash
celery -A cfehome worker -l info
```

### Beat-only (Scheduler-only)
```bash
celery -A cfehome beat -l info
```

### Worker & Beat
```bash
celery -A cfehome worker -l info --beat
```
Using `-l info` is recommended in development, it's optional once in production.


## Turn Functions into Celery Tasks

```python
# myapp/tasks.py

def my_function(a=123, b=None, c=True):
    ...
```
becomes

```python
# myapp/tasks.py
from celery import shared_task

@shared_task
def my_function(a=123, b=None, c=True):
    ...
```
or

```python
# myapp/tasks.py
from celery import shared_task

@shared_task(name="my_function")
def my_function(a=123, b=None, c=True):
    ...
```



## Running Celery Tasks


```python
from myapp.tasks import my_function
```

*Typical*
```python
my_function(a=456, b="Sweet", c=False)
```

*Celery Shortcut*
```python
my_function.delay(a=456, b="Sweet", c=False)
```


*Preferred Celery Call*
```python
delay_seconds = 15
my_function.apply_async(kwargs={"a": 456, "b": "Sweet", "c": False}, countdown=delay_seconds)
```
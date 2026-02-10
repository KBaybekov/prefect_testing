from prefect import flow


def gen():
    yield from [1, 2, 3]
    print('Generator consumed!')


# flow without yielding result
"""
@flow
def _f():
    return gen()
"""
    
@flow
def f():
    yield gen()

generator = next(f())
list(generator)
#f()  # prints 'Generator consumed!'

from prefect import task
from prefect.cache_policies import TASK_SOURCE, INPUTS

# Перезапуск без кэша каждый раз, когда меняется исходный код или входные данные
@task(cache_policy=TASK_SOURCE + INPUTS)
def my_cached_task(x: int):
    return x + 42


# Здесь кэширование не используется при изменении входных данных, за исключением 'debug'
my_custom_policy = INPUTS - 'debug'
@task(cache_policy=my_custom_policy)
def my_cached_task_0(x: int, debug: bool = False):
    print('running...')
    return x + 42


# Здесь используется для кэширования кастомная функция
def static_cache_key(context, parameters):
    # return a constant
    return "static cache key"

@task(cache_key_fn=static_cache_key)
def my_cached_task_1(x: int):
    return x + 1

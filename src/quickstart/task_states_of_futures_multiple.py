from prefect import task, flow


@task
def always_fails_task():
    raise ValueError("I am bad task")


@task
def always_succeeds_task():
    return "foo"


@flow
def always_succeeds_flow():
    return "bar"


@flow
def always_fails_flow():
    x = always_fails_task()
    y = always_succeeds_task()
    z = always_succeeds_flow()
    return x, y, z

always_fails_flow()


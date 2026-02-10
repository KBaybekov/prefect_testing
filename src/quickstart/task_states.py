from prefect import task, flow
from prefect.states import Completed, Failed


@task
def toggle_task(fail: bool):
    if fail:
        return Failed(message="I was instructed to fail.")
    else:
        return Completed(message="I was instructed to succeed.")


@flow
def example():
    # this run will be set to a `Failed` state
    state_one = toggle_task(fail=True)

    # this run will be set to a `Completed` state
    state_two = toggle_task(fail=False)

    # similarly, the flow run will fail because we return a `Failed` state
    return state_one, state_two

if __name__ == "__main__":
    example()
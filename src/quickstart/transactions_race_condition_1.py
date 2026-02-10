import threading
import uuid
from prefect import flow, task
from prefect.locking.filesystem import FileSystemLockManager
from prefect.results import ResultStore
from prefect.settings import PREFECT_HOME
from prefect.transactions import IsolationLevel, transaction
import time

# Здесь у нас 2 потока, запускаемых одновременно.
# Однако здесь используется подходящий уровень изоляции, исключающий race condition

@task
def download_data():
    return f"{threading.current_thread().name} is the winner!"


@task
def write_file(contents: str):
    "Writes to a file."
    with open("race-condition.txt", "w") as f:
        f.write(contents)


@flow
def pipeline(transaction_key: str):
    with transaction(
        key=transaction_key,
        isolation_level=IsolationLevel.SERIALIZABLE,
        store=ResultStore(
            lock_manager=FileSystemLockManager(
                lock_files_directory=PREFECT_HOME.value() / "locks"
            )
        ),
    ) as txn:
        if txn.is_committed():
            print("Data file has already been written. Exiting early.")
            return
        data = download_data()
        write_file(data)


if __name__ == "__main__":
    transaction_key = f"race-condition-{uuid.uuid4()}"
    thread_1 = threading.Thread(target=pipeline, name="Thread 1", args=(transaction_key,))
    thread_2 = threading.Thread(target=pipeline, name="Thread 2", args=(transaction_key,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

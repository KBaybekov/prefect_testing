import os
from time import sleep

from prefect import task, flow
from prefect.transactions import transaction

# Прикольно: мы можем длякаждой функции в транзакции прописать 
# поведение при тех или иных результатах выполнения транзакции

@task
def write_file(contents: str):
    "Writes to a file."
    with open("side-effect.txt", "w") as f:
        f.write(contents)


@write_file.on_rollback
def del_file(transaction):
    "Deletes file."
    os.unlink("side-effect.txt")


@task
def quality_test():
    "Checks contents of file."
    with open("side-effect.txt", "r") as f:
        data = f.readlines()

    if len(data) < 2:
        raise ValueError("Not enough data!")


@flow
def pipeline(contents: str):
    with transaction():
        write_file(contents)
        sleep(5) # sleeping to give you a chance to see the file
        quality_test()


if __name__ == "__main__":
    pipeline(contents="hello world")

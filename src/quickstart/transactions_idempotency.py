from prefect import task, flow
from prefect.transactions import transaction

# Единожды проведя такую транзакцию, мы будем уверены, что при повторном ее проведении
# ничего не изменится

@task
def download_data():
    """Imagine this downloads some data from an API"""
    return "some data"


@task
def write_data(data: str):
    """This writes the data to a file"""
    with open("data.txt", "w") as f:
        f.write(data)


@flow(log_prints=True)
def pipeline():
    with transaction(key="download-and-write-data") as txn:
        if txn.is_committed():
            print("Data file has already been written. Exiting early.")
            return
        data = download_data()
        write_data(data)


if __name__ == "__main__":
    pipeline()

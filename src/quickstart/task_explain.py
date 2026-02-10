from prefect import task

@task(log_prints=False) # вот этот переключатель позволяет сохранять в логи print()
def explain_tasks():
    print("run any python code here!")
    print("but maybe just a little bit")

if __name__ == "__main__":
    explain_tasks()


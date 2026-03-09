from airflow.sdk import dag, task

@dag(
    schedule=None,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["simple"],
)
def simple_dag():

    @task
    def print_hello():
        print("Hello, World!")

    print_hello()

simple_dag()
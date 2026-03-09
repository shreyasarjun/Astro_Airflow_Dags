from airflow.sdk import dag, task, Variable
from airflow.providers.http.operators.http import HttpOperator
from airflow.sdk.bases.hook import BaseHook

from datetime import datetime
import os


@dag(
    dag_id="astro_variables_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["astro", "demo"]
)
def astro_variables_demo():

    @task
    def read_environment_variables():
        env = os.getenv("ENV")
        team = os.getenv("TEAM_NAME")
        timeout = os.getenv("API_TIMEOUT")

        print("Environment Variables")
        print(f"ENV: {env}")
        print(f"TEAM_NAME: {team}")
        print(f"API_TIMEOUT: {timeout}")

        return env


    @task
    def read_airflow_variable():
        project = Variable.get("project_name", default="default_project")

        print("Airflow Variable")
        print(f"Project Name: {project}")


    @task
    def read_connection():
        conn = BaseHook.get_connection("my_api_connection")

        print("Connection Details")
        print(f"Host: {conn.host}")
        print(f"Login: {conn.login}")
        print(f"Password: {conn.password}")


    call_api = HttpOperator(
        task_id="call_sample_api",
        http_conn_id="my_api_connection",
        endpoint="get",
        method="GET",
        log_response=True
    )


    env_task = read_environment_variables()
    var_task = read_airflow_variable()
    conn_task = read_connection()

    env_task >> var_task >> conn_task >> call_api


dag_instance = astro_variables_demo()
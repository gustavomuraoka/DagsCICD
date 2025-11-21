from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator

local_tz = pendulum.timezone('America/Sao_Paulo')

default_args: dict = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ["gustavomuraoka15@gmail.com"],
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

DOCKER_URL = Variable.get("DOCKER_URL_ALT", default_var=None)
DOCKER_IMAGE = Variable.get("DOCKER_IMAGE_DATA_ENGINEERING", default_var=None)

with DAG('start_test_cicd',
         default_args=default_args,
         description='Test - First Test',
         start_date=pendulum.datetime(2025, 11, 19, 0, 0, tz="America/Sao_Paulo"),
         schedule_interval="*/2 * * * *",   # Every 2 minutes
         catchup=False,
         tags=['test'],
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1) as dag:

    start_task = DummyOperator(
        task_id='start_task'
    )

    start_test_cicd = DockerOperator(
        task_id="start_test_cicd",
        image=DOCKER_IMAGE,
        api_version="auto",
        network_mode="host",
        docker_url=DOCKER_URL,
        entrypoint=["make", "-C", "/app/src", "testing.first.tests"],
        xcom_all=True,
        force_pull=False,
        mount_tmp_dir=False,
        auto_remove=True,
    )

    end_task = DummyOperator(
        task_id='end_task',
    )

    start_task >> start_test_cicd >> end_task

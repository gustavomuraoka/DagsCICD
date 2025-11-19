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

with DAG('first_tests',
         default_args=default_args,
         description='Test - First Test',
         start_date=None,
         schedule_interval=None,
         catchup=True,
         tags=['betfair'],
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1) as dag:

    start_task = DummyOperator(
        task_id='start_task'
    )

    dag_betfair_odds_s3 = DockerOperator(
        task_id="dag_betfair_odds_s3",
        image=DOCKER_IMAGE,
        api_version="auto",
        network_mode="host",
        docker_url=DOCKER_URL,
        entrypoint=["make", "betfair.betfair_odds_from_s3"],
        xcom_all=True,
        force_pull=True,
        mount_tmp_dir=False,
        auto_remove=True,
    )

    end_task = DummyOperator(
        task_id='end_task',
    )

    start_task >> authenticate_aws >> dag_betfair_odds_s3 >> end_task

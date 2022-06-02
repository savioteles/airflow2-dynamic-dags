import glob
from datetime import date, timedelta
from os import path

import yaml
from airflow import DAG
from airflow.decorators import task


def create_dag(dag_id, schedule_interval, tags, default_args, input):
    with DAG(
            dag_id=dag_id,
            default_args=default_args,
            schedule_interval=schedule_interval,
            catchup=False,
            tags=tags,
            max_active_runs=1) as dag:
        @task
        def extract(input):
            return input

        @task
        def process(input):
            return input

        @task
        def print_input(input):
            print(input)
            return input

        print_input(process(extract(input)))
    return dag


ABSOLUT_PATH = path.dirname(path.abspath(__file__))
CONFIGURATION_FOLDER = f"{ABSOLUT_PATH}/confs"

DEFAULT_CRON_SCHEDULE = "0 0 * * *"

for conf_file in glob.glob(f"{CONFIGURATION_FOLDER}/*.yaml"):
    with open(conf_file, 'r') as stream:
        conf_data = yaml.safe_load(stream)

    owner = conf_data["owner"]

    default_args = {
        "owner": owner,
        "start_date": conf_data.get("start_date", date.today().strftime("%Y-%m-%d")),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 3,
        "retry_delay": timedelta(minutes=1),
    }

    cron_schedule = conf_data.get("cron_schedule", DEFAULT_CRON_SCHEDULE)
    tags = conf_data["tags"]

    input = conf_data["input"]
    dag_id = conf_data.get('dag_id', f'dag-{owner}')
    globals()[dag_id] = create_dag(dag_id, cron_schedule, tags, default_args, input)

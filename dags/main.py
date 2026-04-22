from airflow import DAG
import pendulum 
from datetime import datetime, timedelta
from api.video_stats import get_channel_playlist_id, get_video_ids, save_to_json, extract_video_data
from datawarehouse.dwh import staging_table, core_table
# local timezone 
local_tz = pendulum.timezone("Australia/Sydney") 

# default args 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': "munalbaraili04@gmail.com",
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(minutes=60),
    'start_date': datetime(2024, 6, 1, tzinfo=local_tz),
    # 'end_date': datetime(2024, 6, 30, tzinfo=local_tz),
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='A DAG to produce JSON data from YouTube API and save it to Postgres',
    schedule='0 14 * * *', # this means that the DAG will run every day at 2 PM Sydney time refer to https://crontab.guru/#0_14_*_*_*
    catchup=False
) as dag:

    # define tasks 
    playlist_id = get_channel_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # define dependencies
    # unsupported operand type error is because we are trying to use the bitwise operator >> to define the dependencies between the tasks, but the tasks are not defined as Airflow tasks, they are just regular Python functions, so we need to use the Airflow task decorator to define them as Airflow tasks before we can use the >> operator to define the dependencies between them.

    playlist_id >> video_ids >> extract_data >> save_to_json_task



with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='A DAG to take json to staging and core schema',
    schedule='0 15 * * *', # this means that the DAG will run every day at 3 PM Sydney time refer to https://crontab.guru/#0_14_*_*_*
    catchup=False
) as dag:

    # define tasks 
    update_staging = staging_table()
    update_core = core_table()
    

    # define dependencies
    update_staging >> update_core

# the overall flow of dwh is 
# 1. we will first load the data from the json file into the staging table, and then we will transform the data in the staging table and load it into the core table.
# inside the each table function we will first check if the video id is already present in the table, if it is present then we will update the row with the new values from the json file,
#  and if it is not present then we will insert a new row into the table.

# the core table is same but with transform_data function applied to the staging data before loading it into the core table, and also we will have an additional column in the core table 
# which is video type (short or normal) based on the duration of the video.
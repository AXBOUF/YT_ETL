from airfloq import DAG
import pendulum 
from datetime import datetime, timedata 
from api.video_stats import get_channel_playlist_id, get_video_ids, save_to_json, extract_video_data

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
    video_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(video_data)

    # define dependencies
    playlist_id >> video_ids >> video_data >> save_to_json_task

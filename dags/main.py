from airfloq import DAG
import pendulum 
from datetime import datetime, timedata 
from api.video_stats import get_channel_id, get_video_ids, get_video_stats, save_to_db

# local timezone 
local_tz = pendulum.timezone("Australia/Sydney") 

# default args 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
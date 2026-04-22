from datawarehouse.data_utils import create_schema, create_table, get_all_video_ids, get_conn_cursor, close_conn_cursor
from datawarehouse.data_loading import load_path
from datawarehouse.data_transformation import transform_data
from datawarehouse.data_modification import update_rows, delete_rows, insert_rows

import logging 
from airflow.decorators import dag, task
from datetime import datetime, timedelta

logger = logging.getLogger(__name__) # activate logging
table = 'yt_api'

@task
def staging_table():
    schema = 'staging'
    conn, cur = None, None
    try:
        conn, cur = get_conn_cursor()
        YT_data = load_path()
        create_schema(schema)
        create_table(schema)
        table_ids = get_all_video_ids(cur, schema) # this is to load video ids from table to if already loaded 

        for row in YT_data:
            if len(table_ids) == 0: # if there are no video ids in the table, then we will insert all the rows from the json file into the staging table.
                insert_rows(cur, conn, schema, row)
            else:
                if row['video_id'] in table_ids: # if the video id is already in the table
                    update_rows(cur, conn, schema, row) # then we will update the row in the staging table with the new values from the json file.
                else:
                    # if the video id is present but new 
                    insert_rows(cur, conn, schema, row) # then we will insert the new row into the staging table.
        ids_in_json = [row['video_id'] for row in YT_data] # grepping all video ids from json file to check if there are any video ids in the table that are not present in the json file, and if there are any such video ids, then we will delete those rows from the staging table.
        ids_to_del = set(table_ids) - set(ids_in_json) # this will give us the set of video ids that are present in the table but not present in the json file.

        if ids_to_del:
            delete_rows(cur, conn, schema, ids_to_del)

        logger.info(f"{schema} table updated successfully with data from json file.")
    except Exception as e:
        logger.error(f"Error updating {schema} table: {str(e)}")
        raise e
    finally:
        if conn and cur:
            close_conn_cursor(conn, cur)

@task
def core_table():
    schema = 'core'
    # we are using transform function in core table because we want to transform the data from the staging table before we load it into the core table, and the transformation logic is defined in the transform_data function in the data_transformation.py file. 
    conn, cur = None, None
    try:
        conn, cur = get_conn_cursor()
        create_schema(schema)
        create_table(schema)
        
        table_ids = get_all_video_ids(cur, schema)
        current_video_ids = set() # SMALL COMMENT: this is to keep track of the video ids that we have already processed in the staging table, so that we can avoid processing the same video id multiple times and also to avoid inserting duplicate rows into the core table.
        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall() # if there are millions of rows then try batching it 
        '''
        batching code will look like this:
        batch_size = 1000
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            for row in batch:
                # process each row in the batch
                # transform the row and insert into core table
                # update currrent_video_ids set with the video id of the processed row
                # this way we will be processing the rows in batches of 1000 and we will
        '''
        for row in rows:
            
            current_video_ids.add(row['Video_id']) # this video id is from staging table, and we are adding it to the set of current video ids that we have processed from the staging table.
            if len(table_ids) == 0: # if there are no video ids in the core table, then we will insert all the rows from the staging table into the core table.
                transformed_row = transform_data(row)
                insert_rows(cur, conn, schema, transformed_row)
            else:
                transformed_row = transform_data(row)

                if transformed_row['Video_id'] in table_ids: # if the video id is already in the core table
                    update_rows(cur, conn, schema, transformed_row) # then we will update the row in the core table with the new values from the staging table.
                else:
                    # if the video id is present but new 
                    insert_rows(cur, conn, schema, transformed_row) # then we will insert the new row into the core table.

        ids_to_del = set(table_ids) - current_video_ids # this will give us the set of video ids that are present in the core table but not present in the staging table, and we will delete those rows from the core table because they are no longer present in the staging table, which means they are no longer present in the json file, which means they are no longer relevant for our analysis.
        if ids_to_del:
            delete_rows(cur, conn, schema, ids_to_del)
        logger.info(f"{schema} table updated successfully with transformed data from staging table.")
    except Exception as e:
        logger.error(f"Error updating {schema} table: {str(e)}")
        raise e

    finally:
        if conn and cur:
            close_conn_cursor(conn, cur)




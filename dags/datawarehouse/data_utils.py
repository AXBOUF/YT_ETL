# we will have scripts for schema creation
from airflow.providers.postgres.hooks.postgres import PostgresHook 

from psycopg2.extras import RealDictCursor

table = "yt_api"
def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db") # establish connection to the database using Airflow's PostgresHook ( id are in docker-compose.yaml)
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor) # create a cursor with RealDictCursor to get results as dictionaries
    return conn, cur

def close_conn_cursor(conn, cur):    
    cur.close()
    conn.close()

# the whole point of this file is to have utility functions for database connection and cursor management, so that we can reuse them across our DAGs without repeating code.  

def create_schema(schema):
    conn, cur = get_conn_cursor()
    create_schema_query = f"CREATE SCHEMA IF NOT EXISTS {schema};" # creating a schema for our tables, we can have multiple schemas in a database to organize our tables better.
    cur.execute(create_schema_query)
    conn.commit()
    close_conn_cursor(conn, cur)
    '''
"video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt":snippet['publishedAt'],
                    "duration":content_details['duration'], # might need to add none in case some vid doesnot have it public
                    "viewCount":statistics.get('viewCount',None),
                    "likeCount":statistics.get('likeCount',None),
                    "commentCount":statistics.get('commentCount',None)
    '''
def create_table(schema):
    conn, cur = get_conn_cursor()
    if schema == "staging": # whats a staging schema? its a temporary area where we can store raw data before we transform it and load it into our final tables. 
        #we can have multiple staging tables for different sources or different types of data. 
        # in this case we will have one staging table for our youtube api data, and then we will transform it and load it into our final tables in the public schema. 
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
            "Video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
            "Video_title" TEXT NOT NULL,
            "Upload_date" TIMESTAMP NOT NULL,
            "Duration" VARCHAR(20) NOT NULL,
            "View_Count" INT, 
            "Like_Count" INT,
            "Comment_Count" INT
            );
        """
    else: 
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
            "Video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
            "Video_title" TEXT NOT NULL,
            "Upload_date" TIMESTAMP NOT NULL,
            "Duration" TIME NOT NULL,
            "Video_Type" VARCHAR(30) NOT NULL,
            "View_Count" INT, 
            "Like_Count" INT,
            "Comment_Count" INT
            );
        """
    cur.execute(create_table_query)
    conn.commit()
    close_conn_cursor(conn, cur)

def get_all_video_ids(cur, schema): 
    cur.execute(f'SELECT "Video_id" FROM {schema}.{table};')
    ids = cur.fetchall()
    video_ids = [row['Video_id'] for row in ids]
    return video_ids

    # we didnot use commit get_conn_cursor cur conn in this function because we are only reading data from the database, we are not making any changes to it, so we dont need to commit anything.





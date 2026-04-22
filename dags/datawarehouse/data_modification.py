import logging 

logger = logging.getLogger(__name__)
table = 'yt_api'

def insert_rows(cur, conn, schema, rows):
    try:
        if schema == 'staging':
            video_id = 'video_id'

            cur.execute(f"""
                INSERT INTO {schema}.{table}
                ("Video_id", "Video_title", "Upload_date", "Duration", "View_Count", "Like_Count", "Comment_Count")
                VALUES (%(video_id)s, %(title)s, %(publishedAt)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s) 
            """, row
            ) # (%()s) is a placeholder for the values that we want to insert into the table, and row is a dictionary that contains the actual values that we want to insert.

        else:
            video_id = 'Video_id'

            cur.execute(f"""
                INSERT INTO {schema}.{table}
                ("Video_id", "Video_title", "Upload_date", "Duration", "Video_Type", "View_Count", "Like_Count", "Comment_Count")
                VALUES (%(Video_id)s, %(Video_title)s, %(Upload_date)s, %(Duration)s, %(Video_Type)s, %(View_Count)s, %(Like_Count)s, %(Comment_Count)s
            """, row # WHY IS ROW HERE? BECAUSE WE ARE PASSING THE VALUES THAT WE WANT TO INSERT INTO THE TABLE, AND ROW IS A DICTIONARY THAT CONTAINS THE ACTUAL VALUES THAT WE WANT TO INSERT.
            ) # HERE THE VALUES ARE MAPPING THE STAGING TABLES 
        conn.commit()
        logger.info(f"Inserted row with video_id: {row[video_id]}")

    except Exception as e:
        logger.error(f"Error loading the row with video_id: {row[video_id]} ")
        raise e

def update_rows(cur, conn, schema, rows):
    try:
        # staging
        if schema == 'staging': # LEFT IS STAGING COLUMN NAMES AND RIGHT IS JSON KEY NAMES
            Video_id = 'video_id'
            Upload_date = 'publishedAt'
            Video_title = 'title'
            View_Count = 'viewCount'
            Like_Count = 'likeCount'
            Comment_Count = 'commentCount'
        else:
            #core # LEFT IS CORE COLUMN NAMES AND RIGHT IS STAGING COLUMN NAMES
            Video_id = 'Video_id'
            Video_title = 'Video_title'
            Upload_date = 'Upload_date'
            Duration = 'Duration'
            Video_Type = 'Video_Type'
            View_Count = 'View_Count'
            Like_Count = 'Like_Count'
            Comment_Count = 'Comment_Count'
        cur.execute(
            f"""
            UPDATE {schema}.{table}
            SET "Video_Title" = %(Video_title)s,
                "Likes_Count" = %(Like_Count)s,
                "View_Count" = %(View_Count)s,
                "Comment_Count" = %(Comment_Count)s
            WHERE "Video_id" = %(Video_id)s AND "Upload_date" = %(Upload_date)s
            """, row # row is for the values that we want to update in the table, and row is a dictionary that contains the actual values that we want to update.
        )
        conn.commit()
        logger.info(f"Updated row with video_id: {row[Video_id]}")
    except Exception as e:
        logger.error(f"Error updating the row with video_id: {row[Video_id]} ")
        raise e

def delete_rows(cur, conn, schema, video_id):
    try:
        ids_to_del = ', '.join([f"'{id}'" for id in video_id]) # we are joining the video ids with a comma and a space, and we are also adding single quotes around each video id because we are using them in the SQL query.
        cur.execute(
            f"""
            DELETE FROM {schema}.{table}
            WHERE "Video_id" IN ({ids_to_del})
            """
        )
        conn.commit()
        logger.info(f"Deleted rows with video_id: {ids_to_del}")
    
    except Exception as e:
        logger.error(f"Error deleting rows with video_id: {ids_to_del} - {str(e)}")
        raise e


            


        
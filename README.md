# YT_ETL

Plan your project start to end in rough vision.

#### Step 1

PLAYLIST ID , VIDEO ID

NOTE

requirement -- for .py scripts

requirements.txt for airflow sth like that

## DOCKER COMMANDS

docker compose up -d ( will run the docker )

docker ps ( shows running conatiner )

docker ps -a ( will show all )

docker exec -it containernames bash ( takes you inside the conatiner )

to check if the data are in both env just go in one and check in there

docker compose up -d --build ( to update with out stopping the )

# NOTE

YOU MISSED THE REQUIREMENTS.TXT CONTENT THAT CAUSED HASSLE TO CREATE

for the airflow we use hooks

connection allows connection with warehouse and cursor allows fucntions

helper functions are small fun that assists

## duration in youtube video contentDetails

The length of the video. The property value is an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) duration. For example, for a video that is at least one minute long and less than one hour long, the duration is in the format `PT#M#S`, in which the letters `PT` indicate that the value specifies a period of time, and the letters `M` and `S` refer to length in minutes and seconds, respectively. The `#` characters preceding the `M` and `S` letters are both integers that specify the number of minutes (or seconds) of the video. For example, a value of `PT15M33S` indicates that the video is 15 minutes and 33 seconds long.

If the video is at least one hour long, the duration is in the format `PT#H#M#S`, in which the `#` preceding the letter `H` specifies the length of the video in hours and all of the other details are the same as described above. If the video is at least one day long, the letters `P` and `T` are separated, and the value's format is `P#DT#H#M#S`. Please refer to the ISO 8601 specification for complete details.

## how does the dwh work



the overall flow of dwh is

1. we will first load the data from the json file into the staging table, and then we will transform the data in the staging table and load it into the core table.

inside the each table function we will first check if the video idis already present in the table, if it is present then we will update the row with the new values from the json file,

andif it isnot present then we will insert a new row into the table.

the core table is same but with transform_data function applied to the staging data before loading it into the core table, and also we will have an additional column in the core table

which is video type (short or normal) based on the duration of the video.



### dag error 

The first error was in [main.py](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html): [playlist_id &gt;&gt; video_ids](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) failed because [playlist_id](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) was a plain string and [video_ids](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) was a plain list, not Airflow task objects. That produced the original `TypeError: unsupported operand type(s) for >>: 'str' and 'list'`.

After that, the `update_db` DAG failed in [data_utils.py](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) because Postgres treated `Video_id` as lowercase [video_id](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) in SQL, but the table column was created as mixed-case `"Video_id"`. That caused `column "video_id" does not exist`.

Then the staging task failed in [data_modification.py](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) with `KeyError: 'Video_id'`. The JSON data uses lowercase [video_id](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html), but the code was trying to read [row[&#34;Video_id&#34;]](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html) when logging or inserting staging rows.

So the pattern was not one single issue. It was a chain of mismatches:

* Airflow task wiring was wrong in [main.py](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html)
* SQL column casing was wrong in [data_utils.py](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html)
* JSON key casing was wrong in [data_modification.py](vscode-file://vscode-app/usr/lib/code/out/vs/code/electron-browser/workbench/workbench.html)

The current code has been adjusted for those issues, so the next DAG run should get past the exact failures shown in the logs.


## Some PSQL Common Commands

Connect to a database:
psql -h localhost -p 5433 -U postgres -d elt_db

List databases:
\l

List schemas:
\dn

List tables:
\dt
\dt staging.*
\dt core.*

Describe a table:
\d staging.yt_api
\d core.yt_api

Show current connection info:
\conninfo

Run a SQL query:
SELECT * FROM staging.yt_api LIMIT 5;

Switch database inside psql:
\c elt_db

Show table data in expanded view:
\x

Quit psql:
\q

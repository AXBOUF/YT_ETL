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

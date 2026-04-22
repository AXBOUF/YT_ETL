import json 
from datetime import date
from pathlib import Path
from glob import glob
import logging

logger = logging.getLogger(__name__) # activate logging

def load_path(): # loading json to variable 
    data_dir = Path(__file__).resolve().parents[2] / "data"
    file_path = data_dir / f"YT_data_{date.today().isoformat()}.json"

    if not file_path.exists():
        matches = sorted(glob(str(data_dir / f"YT_data_{date.today().isoformat()}*.json")))
        if matches:
            file_path = Path(matches[-1])

    try:
        logger.info(f"Processing file: {file_path.name}")

        with open(file_path, 'r', encoding='utf-8') as raw_data:
            data = json.load(raw_data)

        return data 

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise 
    except json.JSONDecodeError: # why try this line because if the json file is not properly formatted, it will raise a JSONDecodeError, and we want to catch that error and log it as well.
        logger.error(f"Error decoding JSON from file: {file_path}")
        raise

    '''
    This function is responsible for loading the data from the json file that we have created in the previous step, and then we will use this data to load it into our database.
    We are using logging to log the progress of our data loading process, and also to log any errors that might occur during the process.
    We are also using exception handling to catch any errors that might occur during the file loading process, such as file not found or json decoding errors, and we are logging those errors as well.
    '''
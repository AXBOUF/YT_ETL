import logging
from airflow.operators.bash import BashOperator

logger = logging.getLogger(__name__)
SODA_CHECK_PATH = "/opt/airflow/include/soda/"
DATASOURCE = "pg_datasource"

def run_soda_checks(schema):
    try:
        task = BashOperator(
            task_id=f'soda_test{schema}',
            bash_command=f'soda scan -d {DATASOURCE} -c {SODA_CHECK_PATH}configuration.yaml -v SCHEMA={schema} {SODA_CHECK_PATH}check.yaml',
        )
        return task
    except Exception as e:
        logger.error(f"Error running Soda checks for {schema} schema: {str(e)}")
        raise e
# the whole flow of syntax is that we are defining a function called run_soda_checks which takes a schema as an argument, 
# and then we are using the BashOperator to run the Soda checks for that schema, and we are passing the configuration file 
# and the check file as arguments to the soda scan command, and we are also passing the datasource name as an argument to the 
# soda scan command, and we are also using logging to log any errors that might occur during the execution of the Soda checks.

import requests
import pytest
import psycopg2
from airflow.models import Connection

def test_youtube_api_response(airflow_variable):
    api_key = airflow_variable("API_KEY")
    channel_handle = airflow_variable("CHANNEL_HANDLE")
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}" 
    try:

        response = requests.get(url)
        assert response.status_code == 200
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API request failed: {e}")

# so the variable we named in conftest.py for def airflow_variable is airflow_variable, but in the test function we are calling it as airflow_variable("API_KEY") and airflow_variable("CHANNEL_HANDLE"), how does that work ?
# the airflow_variable fixture is a function that takes a parameter (whateverthefuck) and returns the value of the Airflow Variable that corresponds to that parameter. 
# when we call
# so the var naming in that function and this function have no relation, we can name the parameter in the airflow_variable fixture whatever we want, it does not have to be whateverthefuck, it can be anything.
# the key is that when we call airflow_variable("API_KEY"), it will pass "API_KEY" as the parameter to the airflow_variable fixture, which will then use that parameter to look up the corresponding Airflow Variable and return its value. 
# so in this case, when we call

def test_real_postgres_connection(real_postgres_connection):
    cursor = None
    try:
        cursor = real_postgres_connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        assert result[0] == 1
    except psycopg2.Error as e:
        pytest.fail(f"Database connection or query failed: {e}")
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()
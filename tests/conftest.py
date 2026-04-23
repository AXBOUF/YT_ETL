import os 
import pytest
from unittest import mock 
from airflow.models import Variable, Connection

@pytest.fixture
def api_key():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_API_KEY = "test_api_key"):
        yield Variable.get("API_KEY")

@pytest.fixture
def channel_handle():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_CHANNEL_HANDLE = "test_channel_key"):
        yield Variable.get("CHANNEL_HANDLE")

@pytest.fixture
def mock_postgres_conn_vars():
    conn = Connection(
        login="test_user",
        password="test_password",
        host="localhost",
        port=5432,
        schema="test_schema" # schema is the db name 
    )
    conn_uri = conn.get_uri()
    with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES_DB_YT_ELT=conn_uri):
        yield Connection.get_connection_from_secrets(conn_id="POSTGRES_DB_YT_ELT")

'''
wtf is going on in this tests directory conftest.py file?
This file is a conftest.py file for pytest, which is used to define fixtures that can be used across multiple test files in the tests directory.
But why are we mocking environment variables and Airflow Variables in this file?
We are mocking environment variables and Airflow Variables in this file because the code in the dags/main.py file relies on these variables to function properly, 
and we want to ensure that our tests can run without actually needing to set these variables in the environment or in Airflow. By mocking these variables,
we can provide test values for them and ensure that our tests can run successfully without any issues related to missing or incorrect variables.

so we are running a mock funtion and running it to return the same function ? are we not just returning the same function without mocking it ?
No, we are not just returning the same function without mocking it. We are using the mock.patch.dict function to temporarily set the environment variables and Airflow Variables 
to specific test values for the duration of the test. This allows us to simulate the presence of these variables without actually needing to set them in the environment or in Airflow. 
The yield statement is used to return the value of the variable after the mock has been applied, and once the test is complete, the mock will be automatically removed and the environment 
variables and Airflow Variables will return to their original state. This way, we can ensure that our tests can run successfully without any issues related to missing or incorrect variables, 
while also allowing us to test the functionality of the code in the dags/main.py file that relies on these variables.

Explanation for donkey would be that we are using the mock.patch.dict function to temporarily set the environment variables and 
Airflow Variables to specific test values for the duration of the test. # so airflow variables are also mocked ?

This allows us to simulate the presence of these variables without actually needing to set them in the environment or in Airflow.
The yield statement is used to return the value of the variable after the mock has been applied, and once the test is complete,
the mock will be automatically removed and the environment variables and Airflow Variables will return to their original state.
This way, we can ensure that our tests can run successfully without any issues related to missing or incorrect variables, while also
allowing us to test the functionality of the code in the dags/main.py file that relies on these variables.


# the whole flow of test is to 
# 1. mock the environment variables and Airflow Variables that are used in the code in the dags/main.py file,
# 2. mock the Postgres connection variables that are used in the code in the dags/main.py file, and then 
# 3. run the tests that are defined in the test files in the tests directory, which will use these mocked variables to test the functionality of the code in the dags/main.py file.

'''
def test_api_key(api_key):
    assert api_key == "test_api_key"

def test_channel_handle(channel_handle):
    assert channel_handle == "test_channel_handle"

def test_postgres_conn(mock_postgres_conn_vars):
    conn = mock_postgres_conn_vars
    assert conn.login == "test_user"
    assert conn.password == "test_password"
    assert conn.schema == "test_schema"
    assert conn.host == "localhost"
    assert conn.port == 5432

def test_dags_integrity(dagbag):
    assert dagbag.import_errors == {}, f"Import errors: {dagbag.import_errors}"
    print("=======")
    print(dagbag.import_errors)

    expected_dags = {'produce_json', 'update_db', 'soda_check'}
    loaded_dags = list(dagbag.dags.keys())
    print("=======")
    print(dagbag.dags.keys())

    for dag_id in expected_dags:
        assert dag_id in loaded_dags, f"DAG '{dag_id}' not found in DAG bag. Loaded DAGs: {loaded_dags}"

    assert dagbag.size() == 3
    print("All expected DAGs are present in the DAG bag.")
    print(dagbag.size())

    expected_task_counts = {
        'produce_json': 5,
        'update_db': 3,
        'soda_check': 2
    }
    for dag_id, dag in dagbag.dags.items():
        expected_count = expected_task_counts[dag_id]
        actual_count = len(dag.tasks)
        assert (
            expected_count == actual_count
        ), f"DAG {dag_id} had {actual_count} tasks, expected {expected_count}."
        print(dag_id, len(dag.tasks))

# the key reason to have test_dags_integrity test is to ensure that all the DAGs that we have defined in our dags/main.py file are being properly loaded into the Airflow DAG bag without any import errors, and that they contain the expected number of tasks. This helps us catch any issues with our DAG definitions early on and ensures that our DAGs are set up correctly before we try to run them in Airflow.

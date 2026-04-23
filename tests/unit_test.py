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
    
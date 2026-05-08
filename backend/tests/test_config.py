import backend.app.core.config as config


def test_build_connection_string_from_env(monkeypatch):
    monkeypatch.setenv("AZURE_SQL_SERVER", "server.database.windows.net,1433")
    monkeypatch.setenv("AZURE_SQL_DATABASE", "testdb")
    monkeypatch.setenv("AZURE_SQL_USERNAME", "testuser")
    monkeypatch.setenv("AZURE_SQL_PASSWORD", "secret")
    monkeypatch.setenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_string = config._build_connection_string()

    assert connection_string.startswith("mssql+pyodbc://")
    assert "server.database.windows.net" in connection_string
    assert "testdb" in connection_string


def test_build_connection_string_missing_env(monkeypatch):
    for key in [
        "AZURE_SQL_SERVER",
        "AZURE_SQL_DATABASE",
        "AZURE_SQL_USERNAME",
        "AZURE_SQL_PASSWORD",
    ]:
        monkeypatch.delenv(key, raising=False)

    assert config._build_connection_string() == ""


def test_api_version_is_defined():
    assert config.API_VERSION == "0.1.0"

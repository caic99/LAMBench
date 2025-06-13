import importlib
from sqlalchemy import Column, Float


def test_default_sqlite(monkeypatch, tmp_path):
    # Remove MySQL env vars if present
    for key in [
        "MYSQL_USERNAME",
        "MYSQL_PASSWORD",
        "MYSQL_HOST",
        "MYSQL_DATABASE_NAME",
    ]:
        monkeypatch.delenv(key, raising=False)
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("LAMBENCH_SQLITE_PATH", str(db_file))

    # Reload base_table with the new environment
    import lambench.databases.base_table as base_table

    importlib.reload(base_table)

    class DummyRecord(base_table.BaseRecord):
        __tablename__ = "dummy"
        value = Column(Float)

    # Perform operations using the sqlite database
    rec = DummyRecord(model_name="m", task_name="t", value=1.0)
    rec.insert()
    assert DummyRecord.count(model_name="m") == 1
    records = DummyRecord.query(model_name="m")
    assert len(records) == 1
    assert records[0].value == 1.0
    # Database file should exist
    assert db_file.exists()

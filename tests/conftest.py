import pytest
from fastapi.testclient import TestClient
from app.main import app
from database.database import get_db, create_tables
import sqlite3
import os
import sys
# Get the parent directory of conftest.py
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

@pytest.fixture(scope="module")
def test_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    create_tables(conn, testing=True)
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        except Exception as e:
            print(e) 
            raise
        # finally:
        #     test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # test_db.close()
    app.dependency_overrides.clear()
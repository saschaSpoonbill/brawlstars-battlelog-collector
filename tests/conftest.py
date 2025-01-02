import pytest
import os
from pathlib import Path
from unittest.mock import patch

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Setzt Test-Umgebungsvariablen"""
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_PORT', '3306')
    monkeypatch.setenv('DB_NAME', 'test_brawlstars')
    monkeypatch.setenv('DB_USER', 'test_user')
    monkeypatch.setenv('DB_PASSWORD', 'test_password')
    monkeypatch.setenv('BRAWLSTARS_API_KEY', 'test_api_key') 

@pytest.fixture(autouse=True)
def mock_db_connection():
    """Mock für die Datenbankverbindung in allen Tests"""
    with patch('mysql.connector.connect') as mock:
        yield mock 
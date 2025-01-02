import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from brawlstars_tracker.services.db_service import BattleLogDB

@pytest.fixture
def db_service():
    with patch('brawlstars_tracker.services.db_service.get_db_connection') as mock_conn:
        # Mock-Verbindung erstellen
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        mock_conn.return_value = connection
        
        db = BattleLogDB()
        db.cursor.execute.return_value = True
        db.connection.commit.return_value = None
        return db

@pytest.fixture
def sample_battle_data():
    return {
        'player_tag': '#2G9LP20YV0',
        'battle_time': datetime.now(),
        'brawler_id': 16000009,
        'brawler_name': 'DYNAMIKE',
        'brawler_power': 7,
        'brawler_trophies': 500,
        'brawler_trophy_change': 8,
        'player_name': 'Spoony',
        'event_id': 15000518,
        'event_mode': 'gemGrab',
        'event_map': 'Hard Rock Mine',
        'battle_mode': 'gemGrab',
        'battle_type': 'ranked',
        'battle_result': 'victory',
        'battle_duration': 156,
        'trophy_change': 8,
        'rank': None,
        'is_star_player': True
    }

def test_insert_battle_log(db_service, sample_battle_data):
    """Test für das Einfügen eines Battle Logs"""
    result = db_service.insert_battle_log(sample_battle_data)
    assert result == True
    # Überprüfen ob execute aufgerufen wurde
    db_service.cursor.execute.assert_called_once() 
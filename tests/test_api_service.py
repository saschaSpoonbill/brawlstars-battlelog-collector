import pytest
import json
from pathlib import Path
from brawlstars_tracker.services.api_service import BrawlStarsAPI

@pytest.fixture
def sample_battle_log():
    """Lädt Test-Battle-Log-Daten aus der JSON-Datei"""
    sample_data_path = Path(__file__).parent / 'data' / 'sample_battle_log.json'
    with open(sample_data_path, 'r') as f:
        return json.load(f)

@pytest.fixture
def api_service():
    return BrawlStarsAPI()

def test_parse_battle_log_team_mode(api_service, sample_battle_log):
    """Test für die Verarbeitung eines Team-Modus Kampfes"""
    player_tag = "2G9LP20YV0"
    processed_battles = api_service.parse_battle_log(sample_battle_log, player_tag)
    
    assert len(processed_battles) > 0
    battle = processed_battles[0]
    
    assert battle['player_tag'] == f"#{player_tag}"
    assert 'battle_time' in battle
    assert 'brawler_id' in battle
    assert 'battle_mode' in battle 
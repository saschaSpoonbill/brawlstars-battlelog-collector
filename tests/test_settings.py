import pytest
import json
from pathlib import Path
from brawlstars_tracker.config.settings import Settings

@pytest.fixture
def temp_players_file(tmp_path):
    """Erstellt eine temporäre players.json für Tests"""
    players_file = tmp_path / "players.json"
    test_data = {
        "players": [
            {
                "tag": "#TEST123",
                "name": "TestPlayer",
                "active": True
            }
        ]
    }
    players_file.write_text(json.dumps(test_data))
    return players_file

def test_load_player_tags(temp_players_file, monkeypatch):
    """Test für das Laden der Spieler-Tags"""
    monkeypatch.setattr('brawlstars_tracker.config.settings.PLAYERS_FILE', temp_players_file)
    
    tags = Settings.load_player_tags()
    assert len(tags) == 1
    assert tags[0] == "#TEST123"

def test_add_player(temp_players_file, monkeypatch):
    """Test für das Hinzufügen eines neuen Spielers"""
    monkeypatch.setattr('brawlstars_tracker.config.settings.PLAYERS_FILE', temp_players_file)
    
    Settings.add_player("#TEST456", "NewPlayer", True)
    
    with open(temp_players_file, 'r') as f:
        data = json.load(f)
    
    assert len(data["players"]) == 2
    assert any(p["tag"] == "#TEST456" for p in data["players"]) 
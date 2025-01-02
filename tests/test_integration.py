import pytest
from datetime import datetime
from brawlstars_tracker.services.api_service import BrawlStarsAPI
from brawlstars_tracker.services.db_service import BattleLogDB
from brawlstars_tracker.config.settings import Settings

def test_full_pipeline():
    """Test der gesamten Pipeline von API-Abruf bis Datenbankschreiben"""
    # Lade Test-Spieler
    player_tags = Settings.load_player_tags()
    assert len(player_tags) > 0, "Keine Spieler in der Konfiguration gefunden"
    
    # API-Abruf
    api = BrawlStarsAPI()
    battle_log_data = api.get_battle_log(player_tags[0])
    assert battle_log_data is not None, "Keine Battle Log Daten empfangen"
    
    # Verarbeite Daten
    processed_battles = api.parse_battle_log(battle_log_data, player_tags[0].strip('#'))
    assert len(processed_battles) > 0, "Keine Kämpfe zum Verarbeiten"
    
    # Speichere in Datenbank
    with BattleLogDB() as db:
        successful_inserts = db.insert_many_battle_logs(processed_battles)
        assert successful_inserts > 0, "Keine Kämpfe in die Datenbank eingefügt" 
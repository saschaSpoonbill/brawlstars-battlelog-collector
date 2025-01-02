import os
import time
from datetime import datetime
from dotenv import load_dotenv
from brawlstars_tracker.services.api_service import BrawlStarsAPI
from brawlstars_tracker.services.db_service import BattleLogDB
from brawlstars_tracker.config.settings import Settings

load_dotenv()

def process_player_battles(player_tag):
    """
    Ruft Battle Logs für einen Spieler ab und speichert sie in der Datenbank.
    
    Args:
        player_tag (str): Spieler-Tag (mit oder ohne #)
        
    Returns:
        tuple: (Anzahl neue Kämpfe, Anzahl verarbeitete Kämpfe)
    """
    api = BrawlStarsAPI()
    
    # Battle Log von der API abrufen
    battle_log_data = api.get_battle_log(player_tag)
    if not battle_log_data:
        print(f"Keine Battle Log Daten für Spieler {player_tag} gefunden")
        return 0, 0
    
    # Battle Log Daten verarbeiten
    processed_battles = api.parse_battle_log(battle_log_data, player_tag.strip('#'))
    if not processed_battles:
        print(f"Keine Kämpfe zum Verarbeiten für Spieler {player_tag}")
        return 0, 0
    
    # In Datenbank speichern
    with BattleLogDB() as db:
        successful_inserts = db.insert_many_battle_logs(processed_battles)
        
    return successful_inserts, len(processed_battles)

def main():
    """
    Hauptfunktion zum Abrufen und Speichern von Battle Logs.
    """
    # Lade Spieler-Tags aus der Konfiguration
    player_tags = Settings.load_player_tags()
    
    print(f"Geladene Spieler-Tags: {player_tags}")
    
    if not player_tags:
        print("Keine aktiven Spieler-Tags gefunden!")
        return
    
    total_new_battles = 0
    total_processed = 0
    
    print(f"Start Battle Log Verarbeitung: {datetime.now()}")
    
    for player_tag in player_tags:
        try:
            print(f"\nVerarbeite Spieler {player_tag}...")
            new_battles, processed = process_player_battles(player_tag)
            total_new_battles += new_battles
            total_processed += processed
            
            print(f"Spieler {player_tag}: {new_battles} neue Kämpfe von {processed} verarbeitet")
            
            # Kurze Pause zwischen API-Aufrufen um Rate Limits zu vermeiden
            time.sleep(1)
            
        except Exception as e:
            print(f"Fehler bei der Verarbeitung von Spieler {player_tag}: {e}")
            continue
    
    print(f"\nVerarbeitung abgeschlossen: {datetime.now()}")
    print(f"Gesamt neue Kämpfe: {total_new_battles}")
    print(f"Gesamt verarbeitet: {total_processed}")

if __name__ == "__main__":
    main() 
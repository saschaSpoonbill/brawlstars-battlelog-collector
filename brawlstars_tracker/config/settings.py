import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Basis-Verzeichnis des Projekts (ein Verzeichnis über src/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Pfad zur players.json Datei
PLAYERS_FILE = BASE_DIR / 'config' / 'players.json'

class Settings:
    @staticmethod
    def load_player_tags():
        """
        Lädt die Spieler-Tags aus der Konfigurationsdatei.
        
        Returns:
            list: Liste der Spieler-Tags
        """
        try:
            print(f"Versuche players.json zu laden von: {PLAYERS_FILE}")
            if not PLAYERS_FILE.exists():
                print("players.json nicht gefunden, erstelle Standard-Konfiguration")
                # Erstelle Standard-Konfiguration wenn Datei nicht existiert
                default_players = {
                    "players": [
                        {
                            "tag": "#2G9LP20YV0",
                            "name": "Spoony",
                            "active": True
                        }
                    ]
                }
                Settings.save_player_tags(default_players["players"])
                return [p["tag"] for p in default_players["players"] if p.get("active", True)]
            
            with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Geladene Daten: {data}")
                # Nur aktive Spieler zurückgeben
                return [p["tag"] for p in data["players"] if p.get("active", True)]
                
        except Exception as e:
            print(f"Fehler beim Laden der Spieler-Tags: {e}")
            return []

    @staticmethod
    def save_player_tags(players):
        """
        Speichert die Spieler-Tags in der Konfigurationsdatei.
        
        Args:
            players (list): Liste der Spieler-Daten
        """
        try:
            # Stelle sicher, dass das Verzeichnis existiert
            PLAYERS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(PLAYERS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"players": players}, f, indent=4)
                
        except Exception as e:
            print(f"Fehler beim Speichern der Spieler-Tags: {e}")

    @staticmethod
    def add_player(tag, name="", active=True):
        """
        Fügt einen neuen Spieler zur Konfiguration hinzu.
        
        Args:
            tag (str): Spieler-Tag
            name (str): Spielername (optional)
            active (bool): Ob der Spieler aktiv verfolgt werden soll
        """
        try:
            current_players = []
            if PLAYERS_FILE.exists():
                with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    current_players = data["players"]
            
            # Prüfe ob Spieler bereits existiert
            for player in current_players:
                if player["tag"] == tag:
                    player["name"] = name
                    player["active"] = active
                    break
            else:
                # Füge neuen Spieler hinzu
                current_players.append({
                    "tag": tag,
                    "name": name,
                    "active": active
                })
            
            Settings.save_player_tags(current_players)
            
        except Exception as e:
            print(f"Fehler beim Hinzufügen des Spielers: {e}") 
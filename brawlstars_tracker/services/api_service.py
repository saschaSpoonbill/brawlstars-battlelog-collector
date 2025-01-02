import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BrawlStarsAPI:
    def __init__(self):
        self.api_key = os.getenv('BRAWLSTARS_API_KEY')
        self.base_url = 'https://api.brawlstars.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

    def get_battle_log(self, player_tag):
        """
        Ruft das Battle Log eines Spielers ab.
        """
        player_tag = player_tag.strip('#')
        
        try:
            response = requests.get(
                f'{self.base_url}/players/%23{player_tag}/battlelog',
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            print(f"API-Antwort erhalten: {len(data.get('items', []))} Kämpfe gefunden")  # Debug-Ausgabe
            return data
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen des Battle Logs: {e}")
            return None

    def parse_battle_log(self, battle_log_data, player_tag):
        """
        Verarbeitet die Battle Log Daten in ein Format für die Datenbank.
        """
        processed_battles = []
        
        for item in battle_log_data.get('items', []):
            try:
                battle_time = datetime.strptime(
                    item['battleTime'], 
                    '%Y%m%dT%H%M%S.%fZ'
                )
                
                battle = item['battle']
                event = item.get('event', {})
                
                # Debug-Ausgaben
                print(f"\nVerarbeite Kampf vom {battle_time}")
                print(f"Kampfmodus: {battle.get('mode')}")
                
                base_battle_info = {
                    'player_tag': f'#{player_tag}',
                    'battle_time': battle_time,
                    'event_id': event.get('id'),
                    'event_mode': event.get('mode'),
                    'event_map': event.get('map'),
                    'battle_mode': battle.get('mode'),
                    'battle_type': battle.get('type'),
                    'battle_result': battle.get('result'),
                    'battle_duration': battle.get('duration'),
                    'trophy_change': battle.get('trophyChange'),
                    'rank': battle.get('rank')
                }

                # Finde den verfolgten Spieler und seine Brawler
                if 'teams' in battle:
                    # Team-basierte Modi
                    for team in battle['teams']:
                        for player in team:
                            if player['tag'].strip('#') == player_tag:
                                processed_battles.append(self._process_player_data(
                                    player, 
                                    base_battle_info,
                                    battle.get('starPlayer', {}).get('tag') == player['tag']
                                ))
                                print(f"Team-Modus: Spieler gefunden mit Brawler {player['brawler']['name']}")
                
                elif 'players' in battle:
                    # Duell oder andere Modi mit einzelnen Spielern
                    for player in battle['players']:
                        if player['tag'].strip('#') == player_tag:
                            if 'brawlers' in player:
                                # Duelle mit mehreren Brawlern
                                for brawler in player['brawlers']:
                                    battle_info = base_battle_info.copy()
                                    processed_battles.append(self._process_player_data(
                                        {'tag': player['tag'], 
                                         'name': player['name'],
                                         'brawler': brawler},
                                        battle_info,
                                        False
                                    ))
                                    print(f"Duell-Modus: Spieler gefunden mit Brawler {brawler['name']}")
                            else:
                                # Einzelner Brawler
                                processed_battles.append(self._process_player_data(
                                    player,
                                    base_battle_info,
                                    False
                                ))
                                print(f"Einzel-Modus: Spieler gefunden mit Brawler {player['brawler']['name']}")

            except KeyError as e:
                print(f"Fehler beim Verarbeiten des Kampfes: Fehlendes Feld {e}")
                continue
            except Exception as e:
                print(f"Unerwarteter Fehler beim Verarbeiten des Kampfes: {e}")
                continue

        return processed_battles

    def _process_player_data(self, player_data, battle_info, is_star_player):
        """
        Verarbeitet die Spielerdaten für einen einzelnen Eintrag.
        """
        try:
            brawler = player_data['brawler']
            battle_entry = battle_info.copy()
            
            battle_entry.update({
                'player_name': player_data['name'],
                'brawler_id': brawler['id'],
                'brawler_name': brawler['name'],
                'brawler_power': brawler['power'],
                'brawler_trophies': brawler.get('trophies', 0),
                'brawler_trophy_change': brawler.get('trophyChange'),
                'is_star_player': is_star_player
            })
            
            return battle_entry
        except KeyError as e:
            print(f"Fehler beim Verarbeiten der Spielerdaten: Fehlendes Feld {e}")
            print(f"Spielerdaten: {player_data}")
            raise 
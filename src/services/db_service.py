from brawlstars_tracker.config.database import get_db_connection
from mysql.connector import Error

class BattleLogDB:
    def __init__(self):
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor(dictionary=True)

    def insert_battle_log(self, battle_data):
        """
        Fügt einen Battle Log Eintrag in die Datenbank ein.
        Verwendet INSERT IGNORE um Duplikate zu vermeiden.
        
        Args:
            battle_data (dict): Verarbeitete Battle Log Daten
        
        Returns:
            bool: True wenn erfolgreich, False bei Fehler
        """
        query = """
            INSERT IGNORE INTO battle_logs (
                player_tag,
                battle_time,
                brawler_id,
                brawler_name,
                brawler_power,
                brawler_trophies,
                brawler_trophy_change,
                player_name,
                event_id,
                event_mode,
                event_map,
                battle_mode,
                battle_type,
                battle_result,
                battle_duration,
                trophy_change,
                rank,
                is_star_player
            ) VALUES (
                %(player_tag)s,
                %(battle_time)s,
                %(brawler_id)s,
                %(brawler_name)s,
                %(brawler_power)s,
                %(brawler_trophies)s,
                %(brawler_trophy_change)s,
                %(player_name)s,
                %(event_id)s,
                %(event_mode)s,
                %(event_map)s,
                %(battle_mode)s,
                %(battle_type)s,
                %(battle_result)s,
                %(battle_duration)s,
                %(trophy_change)s,
                %(rank)s,
                %(is_star_player)s
            )
        """
        
        try:
            self.cursor.execute(query, battle_data)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Fehler beim Einfügen des Battle Logs: {e}")
            self.connection.rollback()
            return False

    def insert_many_battle_logs(self, battle_logs):
        """
        Fügt mehrere Battle Log Einträge in die Datenbank ein.
        
        Args:
            battle_logs (list): Liste von Battle Log Dictionaries
            
        Returns:
            int: Anzahl der erfolgreich eingefügten Einträge
        """
        successful_inserts = 0
        
        for battle_data in battle_logs:
            if self.insert_battle_log(battle_data):
                successful_inserts += 1
                
        return successful_inserts

    def get_latest_battle_time(self, player_tag):
        """
        Ermittelt den Zeitpunkt des letzten gespeicherten Kampfes für einen Spieler.
        
        Args:
            player_tag (str): Der Spieler-Tag
            
        Returns:
            datetime oder None: Zeitpunkt des letzten Kampfes oder None wenn keine Daten
        """
        query = """
            SELECT MAX(battle_time) as latest_battle
            FROM battle_logs
            WHERE player_tag = %s
        """
        
        try:
            self.cursor.execute(query, (player_tag,))
            result = self.cursor.fetchone()
            return result['latest_battle'] if result else None
        except Error as e:
            print(f"Fehler beim Abrufen der letzten Battle-Zeit: {e}")
            return None

    def close(self):
        """
        Schließt die Datenbankverbindung.
        """
        try:
            self.cursor.close()
            self.connection.close()
        except Error as e:
            print(f"Fehler beim Schließen der Datenbankverbindung: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 
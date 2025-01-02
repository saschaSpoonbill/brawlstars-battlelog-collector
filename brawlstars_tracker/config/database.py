import os
from mysql.connector import connect, Error
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Fehler bei der Datenbankverbindung: {e}")
        raise

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS battle_logs (
                player_tag VARCHAR(50),
                battle_time DATETIME,
                brawler_id INT,
                brawler_name VARCHAR(50),
                brawler_power INT,
                brawler_trophies INT,
                brawler_trophy_change INT,
                player_name VARCHAR(50),
                event_id INT,
                event_mode VARCHAR(50),
                event_map VARCHAR(100),
                battle_mode VARCHAR(50),
                battle_type VARCHAR(50),
                battle_result VARCHAR(10),
                battle_duration INT,
                trophy_change INT,
                `rank` INT,
                is_star_player BOOLEAN,
                PRIMARY KEY (player_tag, battle_time, brawler_id)
            )
        """)
        connection.commit()
    except Error as e:
        print(f"Fehler beim Erstellen der Tabelle: {e}")
        raise
    finally:
        cursor.close()
        connection.close() 
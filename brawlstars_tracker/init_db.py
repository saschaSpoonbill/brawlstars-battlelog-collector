from brawlstars_tracker.config.database import create_tables

if __name__ == "__main__":
    print("Initialisiere Datenbank...")
    create_tables()
    print("Datenbank-Tabellen wurden erstellt!") 
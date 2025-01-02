import schedule
import time
from brawlstars_tracker.main import main as process_battles

def job():
    """
    Führt die Battle Log Verarbeitung aus und fängt Fehler ab.
    """
    try:
        process_battles()
    except Exception as e:
        print(f"Fehler bei der geplanten Ausführung: {e}")

def run_scheduler():
    """
    Startet den Scheduler mit definierten Intervallen.
    """
    # Battle Logs alle 15 Minuten abrufen
    schedule.every(15).minutes.do(job)
    
    print("Scheduler gestartet. Drücken Sie Ctrl+C zum Beenden.")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler wird beendet...")
            break
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")
            # Kurze Pause vor dem nächsten Versuch
            time.sleep(60)

if __name__ == "__main__":
    run_scheduler() 
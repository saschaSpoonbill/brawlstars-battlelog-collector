# Brawl Stars Battle Log Collector

A lightweight data collector for Brawl Stars match data that periodically fetches battle logs from the official Brawl Stars API. The application stores match details in a database, enabling analysis of player performance, trophy changes, and other game statistics.

*Note: While the documentation is in English, the code and program interface are in German.*

## Features
- Automated collection of battle log data
- Storage of match details in a SQLite database
- Track trophy changes and performance metrics
- Easy data export for analysis

## Technical Details

### Requirements
- Python 3.8+
- Brawl Stars Developer API Key
- Required Python packages (see `requirements.txt`):
  - requests
  - sqlite3
  - python-dotenv
  - streamlit (for visualization)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/brawl-stars-battle-log.git
   cd brawl-stars-battle-log
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows:
   .\venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install package in development mode:**
   ```bash
   pip install -e .
   ```

4. **Create configuration file:**
   
   Create a `.env` file with the following settings:
   ```env
   # Brawl Stars API
   BRAWLSTARS_API_KEY=your_api_key_here
   
   # MySQL Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=brawlstars
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   ```

5. **Initialize MySQL database:**
   ```bash
   # Create database
   mysql -u root -p
   CREATE DATABASE brawlstars;
   exit
   
   # Initialize tables
   python -m brawlstars_tracker.init_db
   ```

### Configuration

Players are configured in `config/players.json`.

### Usage

1. **One-time execution:**
   ```bash
   python -m brawlstars_tracker.main
   ```

2. **Continuous execution** (runs every 15 minutes):
   ```bash
   python -m brawlstars_tracker.scheduler
   ```

## Database Schema

The application stores battle logs in a single table with the following structure:
- `player_tag`: Player identifier
- `battle_time`: Time of the battle
- `brawler_id`: Unique identifier of the brawler used
- `brawler_name`: Name of the brawler
- `brawler_power`: Power level of the brawler
- `brawler_trophies`: Trophy count for that brawler
- `battle_mode`: Game mode (e.g., "gemGrab", "brawlBall")
- `battle_result`: Outcome ("victory", "defeat")
- And more...

## Development

Run tests:
bash
pytest tests/

## Author
Sascha / saschaSpoonbill (supported by Claude)  
GitHub: [@saschaSpoonbill](https://github.com/saschaSpoonbill)

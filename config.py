# config.py

NUM_SENSORS = 9
BASE_TEMP = 22.0         # °C
TIME_STEPS = 500
FIRE_ROOM = 1            # Should be between 0 and NUM_SENSORS-1
FIRE_START = 300         # Time step when fire starts
ALERT_THRESHOLD = 55.0   # °C
VOTE_QUORUM = 5          # Minimum votes to confirm fire (out of NUM_SENSORS)

# Digital twin memory window
TWIN_HISTORY_SIZE = 10

# File paths
LEDGER_PATH = "data/ledger.json"
RESULTS_PATH = "data/results.csv"

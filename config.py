# config.py

NUM_SENSORS = 5
BASE_TEMP = 22.0         # °C
TIME_STEPS = 30
FIRE_ROOM = 2
FIRE_START = 10
ALERT_THRESHOLD = 55.0   # °C
VOTE_QUORUM = 3

# Digital twin memory window
TWIN_HISTORY_SIZE = 5

# File paths
LEDGER_PATH = "data/ledger.json"
RESULTS_PATH = "data/results.csv"

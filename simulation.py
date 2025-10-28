# simulation.py
import time
from sensor import Sensor
from blockchain import Blockchain
from config import NUM_SENSORS, TIME_STEPS, VOTE_QUORUM

def run_simulation():
    sensors = [Sensor(i) for i in range(NUM_SENSORS)]
    blockchain = Blockchain()

    print("Starting Smart Home Fire Simulation...\n")

    for t in range(TIME_STEPS):
        votes = []
        for s in sensors:
            s.read_temperature(t)
            votes.append(s.detect_anomaly())

        quorum = sum(votes)
        decision = "🔥 FIRE DETECTED!" if quorum >= VOTE_QUORUM else "✅ Normal operation."
        temps = [round(s.temp, 1) for s in sensors]

        print(f"t={t:02d}s | Temps={temps} | Votes={votes} | {decision}")

        # Create blockchain block
        data = {"time": t, "temps": temps, "votes": votes, "decision": decision}
        blockchain.create_new_block(data)

        time.sleep(0.1)

    print("\nSimulation complete! Ledger written to data/ledger.json.")

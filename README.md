# Real-Time Fabrication Filtering for Smart-Home Safety — Simulation Prototype

A modular Python prototype that simulates a zero-trust smart-home safety system: temperature/smoke sensors + digital twins + lightweight voting consensus + an append-only blockchain ledger.  

Intended for research prototyping and preliminary results for an HCII submission (human-centered evaluation + system performance).

---

## Table of contents

- [What this project does](#what-this-project-does)
    
- [Features](#features)
    
- [Quickstart (run locally)](#quickstart-run-locally)
    
- [Project structure](#project-structure)
    
- [Configuration (`config.py`)](#configuration-configpy)
    
- [How the simulation works (chunk-by-chunk)](#how-the-simulation-works-chunk-by-chunk)
    
- [The lightweight blockchain ledger](#the-lightweight-blockchain-ledger)
    
- [Collecting metrics and example CSV format](#collecting-metrics-and-example-csv-format)
    
- [Visualizing results (suggested scripts)](#visualizing-results-suggested-scripts)
    
- [Experiments to run (suggestions for your paper)](#experiments-to-run-suggestions-for-your-paper)
    
- [Extending toward a real permissioned blockchain (notes)](#extending-toward-a-real-permissioned-blockchain-notes)
    
- [HCI / Human-centered demo suggestions](#hci--human-centered-demo-suggestions)
    
- [Raspberry Pi / deployment notes](#raspberry-pi--deployment-notes)
    
- [Troubleshooting & FAQ](#troubleshooting--faq)
    
- [License, attribution, and suggested citations](#license-attribution-and-suggested-citations)
    

---

## What this project does

- Simulates a small home with multiple temperature/smoke sensors.
    
- Each sensor holds a **Digital Twin** (a lightweight predictive model) to detect deviations.
    
- Sensors vote locally whether an alert (fire) is happening.
    
- A **quorum-based decision rule** aggregates votes to confirm alerts.
    
- Every alert event, the votes, and the final decision are appended into a **local, immutable ledger** (a simple blockchain-like JSON file).
    
- Designed to generate preliminary technical metrics (latency, detection time, false positive rate) and artifacts (ledger entries) you can use in the Methods/Results section of an HCII proposal.
    
- Easily extended to experiment with compromised sensors, reputation scoring, and basic HCI feedback channels.
    

---

## Features

- Modular code (separate files for sensors, digital twin, blockchain, simulation driver, configuration).
    
- Configurable parameters (number of sensors, fire start time, quorum, thresholds).
    
- Local simulated blockchain ledger (`data/ledger.json`) with chained hashes for immutability.
    
- Hooks for metrics collection and plotting.
    
- Designed to run on standard desktop or Raspberry Pi.
    

---

## Quickstart (run locally)

**Prerequisites**

- Python 3.8+ installed.
    
- Optional: `git` and VS Code.
    

**Clone & set up**

```
git clone https://github.com/Fade2BlackOps/smart_home_fire_sim.git 

cd smart_home_fire_sim 

python3 -m venv .venv # activate the venv: 
# Linux / macOS: source .venv/bin/activate 
# Windows (PowerShell): .venv\Scripts\Activate.ps1 

pip install -r requirements.txt
```

**Run the simulation**

`python main.py`

**Output**

- Terminal prints per-timestep sensor temps, votes, and decisions.
    
- `data/ledger.json` populated with block entries (one per timestep).
    
- Create `data/` directory before running if your environment blocks automatic creation.
    

---

## Project structure

```
smart_home_fire_sim/
├── main.py
├── simulation.py
├── blockchain.py
├── sensor.py
├── digital_twin.py
├── config.py
├── flask_app.py         ← NEW Flask dashboard backend
├── templates/
│   └── index.html       ← Front-end HTML (Chart.js + Socket.IO)
└── static/
    ├── main.js          ← Live dashboard logic
    └── style.css        ← Styling
```

---

## Configuration (`config.py`)

Edit `config.py` to run different experiments. Important fields:

```
NUM_SENSORS = 5 
BASE_TEMP = 22.0 
TIME_STEPS = 30 
FIRE_ROOM = 2 
FIRE_START = 10 
ALERT_THRESHOLD = 55.0 
VOTE_QUORUM = 3 
TWIN_HISTORY_SIZE = 5 
LEDGER_PATH = "data/ledger.json" 
RESULTS_PATH = "data/results.csv"
```

**Common experiments**: change `NUM_SENSORS`, `VOTE_QUORUM`, and `ALERT_THRESHOLD` to test sensitivity vs. latency tradeoffs.

---

## How the simulation works (chunk-by-chunk)

1. **`main.py`** — starts the simulation:
    
    - `if __name__ == "__main__": run_simulation()`
        
2. **`simulation.py`** — time loop:
    
    - Creates `NUM_SENSORS` Sensor objects.
        
    - Each timestep:
        
        - Calls `sensor.read_temperature(t)` to simulate environment dynamics (fire room spikes, neighbors warm up).
            
        - Calls `sensor.detect_anomaly()` to determine if that sensor votes `True` (fire) or `False`.
            
        - Aggregates votes; if `sum(votes) >= VOTE_QUORUM` then `FIRE DETECTED`, otherwise normal.
            
        - Creates a new blockchain block with `{ time, temps, votes, decision }`.
            
        - Prints log and optionally writes metrics.
            
3. **`sensor.py`** — Sensor object:
    
    - Holds `temp` (simulated reading) and a `DigitalTwin` instance.
        
    - `read_temperature(t)` models heat spread:
        
        - Fire room: large random increase per timestep.
            
        - Neighbor rooms: moderate increase.
            
        - Other rooms: smaller increases.
            
    - `detect_anomaly()` uses:
        
        - Absolute threshold `ALERT_THRESHOLD`.
            
        - Relative deviation (`current_temp - twin.expected`) > some value (e.g., `20°C` in baseline).
            
    - Returns boolean vote.
        
4. **`digital_twin.py`** — DigitalTwin:
    
    - Maintains short history (rolling window) and computes expected temperature (simple mean).
        
    - `deviation()` returns how far actual reading is from expected.
        
5. **`blockchain.py`** — Local chain:
    
    - `Block(index, timestamp, data, prev_hash)` stores fields and computes `hash = sha256(index,timestamp,data,prev_hash)`.
        
    - `Blockchain.create_new_block(data)` creates a new block, appends to in-memory chain and writes JSON line to `data/ledger.json`.
        
    - Ledger entries include `index`, `timestamp`, `data`, `prev_hash`, `hash`.
        

---

## The lightweight blockchain ledger

Each ledger entry (one per timestep) is a JSON block similar to:

```json
{
  "index": 12,
  "timestamp": "2025-10-07T18:33:12.123456",
  "data": {
    "time": 12,
    "temps": [
      23.0,
      32.0,
      65.0,
      29.8,
      24.5
    ],
    "votes": [
      false,
      true,
      true,
      true,
      false
    ],
    "decision": "🔥 FIRE DETECTED!"
  },
  "prev_hash": "a48b4f...",
  "hash": "c2f7b9..."
}
```


This is a **simulation ledger**: it demonstrates immutability and auditability in the prototype. It is _not_ a drop-in substitute for Hyperledger Fabric; see [Extending](#extending-toward-a-real-permissioned-blockchain-notes).

---

## Collecting metrics and example CSV format

Augment `simulation.py` to record metrics (detection time, false positives, decision latency). Example CSV header:

`trial,fire_start_time,detection_time,false_positive_count,avg_decision_latency,quorum,threshold,num_sensors 1,10,12,0,0.3,3,55.0,5`

Suggested metrics:

- `detection_time` — wall/time-step when quorum first confirmed after `FIRE_START`.
    
- `false_positive_count` — number of quorum confirmations before `FIRE_START`.
    
- `avg_decision_latency` — average per-time-step processing time (if you add simulated network delay or processing time).
    
- `accuracy` — proportion of true events correctly detected vs. missed.
    

You can write CSV lines inside `simulation.py` using Python `csv` or `pandas`.

---

## Visualizing results (suggested scripts)

Use `matplotlib` (or export CSV and use Excel) to plot:

- Sensor temperatures over time (each sensor a different colored line).
    
- Vote count (bars) and vertical markers showing `FIRE_START` and `detection_time`.
    
- Reputation score changes over time (if implemented).
    

Minimal example:

`import matplotlib.pyplot as plt # temps_history is list of lists: [ [t0_s0, t0_s1...], [t1_s0...], ... ] # Convert to per-sensor series and plot`

---

## Experiments to run:

- **Baseline vs. voting**: Compare a single-sensor threshold (baseline) vs. quorum voting. Report false positive reduction and detection latency.
    
- **Quorum sensitivity**: Sweep `VOTE_QUORUM` from 2..N and observe tradeoff (higher quorum → fewer false positives, more delay).
    
- **Compromised sensor**: Mark one sensor compromised (always votes True or randomly) and test detection/false positives and reputation system response.
    
- **Network delays**: add random message latency and timeouts; measure detection time.
    
- **Digital twin strength**: compare rolling average vs. exponential smoothing vs. simple linear predictor.
    
- **HCI mini-study**: show a mock dashboard to 8–12 participants and collect trust scores (Likert), comprehension, and response times.
    

---

## Extending toward a real permissioned blockchain (notes)

This prototype writes a local chained JSON ledger. To integrate with a **real permissioned blockchain** (e.g., Hyperledger Fabric):

- Replace `blockchain.create_new_block(data)` with a Fabric client that submits a transaction to chaincode (smart contract).
    
- Record only metadata (hashes and decisions) on-chain; store raw sensor data off-chain (IPFS or secure cloud) and put hashes on-chain to save space.
    
- Consider transaction latency: Fabric confirmation time will be higher than local file writes — measure and report it in experiments.
    
- You'll need a Fabric test network (peers, orderer, CA), enrollment certificates for validators, and chaincode to accept and validate votes.
    

---

## HCI / Human-centered demo suggestions

- Create a simple web dashboard (Flask + minimal HTML/JS) showing:
    
    - Live sensor temps, vote count, system confidence, explanation text.
        
    - A “Confirm / Deny” prompt for ambiguous events (update ledger with user feedback).
        
- For early user tests, a Figma prototype is fine — show the screenflows and ask participants for trust perceptions.
    

---

## Raspberry Pi / deployment notes

- Python 3.8+ works on Raspberry Pi OS.
    
- Use `tmux` for running multiple validator/sensor processes on multiple Pis.
    
- For low-power Pis (Pi Zero), reduce logging frequency and message size.
    
- If you simulate networked validators, use sockets or MQTT for inter-process messaging and measure real network latency.
    

---

## Troubleshooting & FAQ

- **Ledger file not created**: ensure `data/` exists or the process has write permissions. The blockchain code attempts to create the directory automatically, but permission issues can block it.
    
- **Very slow on Raspberry Pi**: reduce `TIME_STEPS` and `time.sleep()` and avoid plotting on-device.
    
- **I want a GUI**: add Flask and a simple JavaScript front-end to poll for `data/ledger.json` updates (or use WebSockets).
    

---

<!-- ## License, attribution, and suggested citations

You can include this repository and its code in your lab report / proposal. Suggested citation for the prototype (change to your names and year):

> Vasil et al., _Real-Time Fabrication Filtering for Safety Alerts in Smart Homes using Smart Contracts and Lightweight Voting — Prototype_, 2025. (Repository: `smart_home_fire_sim`)

Cite the background papers you used in your literature review (titles provided in your project notes). Example references to include in your proposal:

- “A Semi-Centralized Trust Management Model Based on Blockchain for Data Exchange in IoT System”
    
- “Blockchain-Modeled Edge-Computing-Based Smart Home Monitoring System with Energy Usage Prediction (Sensors 2023)”
    
- “A Blockchain-Based Decentralized, Fair and Authenticated Information Sharing Scheme in Zero Trust IoT”
    
- “Ensuring Zero Trust IoT Data Privacy: Differential Privacy in Blockchain Using Federated Learning” -->
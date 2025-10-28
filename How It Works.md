# How This Simulation Works
| File               | Role                               | Real-world analogy                     |
| ------------------ | ---------------------------------- | -------------------------------------- |
| `config.py`        | Simulation settings                | System parameters / config panel       |
| `digital_twin.py`  | Predicts expected temperature      | Cloud-based “digital twin” model       |
| `sensor.py`        | Simulates IoT device behavior      | Physical smoke/heat sensors            |
| `blockchain.py`    | Records decisions immutably        | Permissioned ledger (Hyperledger-like) |
| `simulation.py`    | Controls time loop, collects votes | IoT network runtime                    |
| `main.py`          | Entry point                        | ADT hub / master controller            |
| `data/ledger.json` | Output ledger                      | Blockchain storage                     |

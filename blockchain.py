# blockchain.py
import json
import hashlib
import os
from datetime import datetime
from config import LEDGER_PATH

class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_ledger()

    def load_ledger(self):
        os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
        if os.path.exists(LEDGER_PATH) and os.path.getsize(LEDGER_PATH) > 0:
            with open(LEDGER_PATH, "r") as f:
                lines = f.readlines()
                for line in lines:
                    self.chain.append(json.loads(line))
        else:
            # Create genesis block
            genesis = Block(0, str(datetime.now()), {"message": "Genesis Block"}, "0")
            self.add_block(genesis)

    def add_block(self, block):
        self.chain.append(block.__dict__)
        with open(LEDGER_PATH, "a") as f:
            f.write(json.dumps(block.__dict__) + "\n")

    def create_new_block(self, data):
        index = len(self.chain)
        prev_hash = self.chain[-1]["hash"] if self.chain else "0"
        block = Block(index, str(datetime.now()), data, prev_hash)
        self.add_block(block)
        return block

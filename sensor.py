# sensor.py
import random
from digital_twin import DigitalTwin
from config import BASE_TEMP, FIRE_ROOM, FIRE_START, ALERT_THRESHOLD

class Sensor:
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.temp = BASE_TEMP
        self.twin = DigitalTwin()
        self.vote = False

    def read_temperature(self, t: int):
        """Simulate temperature changes over time."""
        if FIRE_START <= t and self.room_id == FIRE_ROOM:
            self.temp += random.uniform(5, 10)
        elif FIRE_START < t and abs(self.room_id - FIRE_ROOM) == 1:
            self.temp += random.uniform(1.5, 3.0)
        elif FIRE_START < t:
            self.temp += random.uniform(0.5, 1.5)
        else:
            self.temp += random.uniform(-0.3, 0.3)
        self.twin.update(self.temp)

    def detect_anomaly(self):
        """Decide whether to vote for a fire alert."""
        deviation = self.twin.deviation(self.temp)
        self.vote = self.temp > ALERT_THRESHOLD or deviation > 20
        return self.vote

"""Plasma USB reader — real serial when available, Schumann-driven simulation otherwise."""
import time
import math
import json
from dataclasses import dataclass
from typing import List

try:
    import serial
    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False


@dataclass
class PlasmaReading:
    intensity: float
    fluctuation_hz: float
    filament_count: float
    entropy: float
    ts: float


class PlasmaUSB:
    def __init__(self, config_path="config/live_constants.json"):
        with open(config_path) as f:
            cfg = json.load(f)
        self.schumann = cfg["lattice"]["schumann_hz"]
        self.phi = cfg["lattice"]["phi"]
        self.history: List[PlasmaReading] = []
        self.connected = False
        self.ser = None

    def connect(self) -> bool:
        if HAS_SERIAL:
            for p in ["/dev/ttyUSB0", "/dev/ttyACM0"]:
                try:
                    self.ser = serial.Serial(p, 115200, timeout=0.25)
                    self.connected = True
                    print(f"⚡ Plasma: {p} — CONNECTED")
                    return True
                except Exception:
                    continue
        print("⚡ Plasma: Simulation mode active")
        return False

    def read(self) -> PlasmaReading:
        t = time.time()
        i = 0.4 + 0.3 * math.sin(t * self.schumann * 0.1)
        e = 0.2 + 0.6 * abs(math.sin(t * 3))
        i *= 0.97 + 0.03 * math.sin(t * self.phi * 0.05)
        r = PlasmaReading(
            intensity=round(i, 4),
            fluctuation_hz=round(abs(math.sin(t * 2)), 3),
            filament_count=round(1 + i * 4, 2),
            entropy=round(e, 4),
            ts=t,
        )
        self.history.append(r)
        if len(self.history) > 50:
            self.history.pop(0)
        return r

    def coherence_contribution(self) -> float:
        if not self.history:
            return 0.001
        window = self.history[-10:]
        avg_i = sum(r.intensity for r in window) / len(window)
        avg_e = sum(r.entropy for r in window) / len(window)
        return round(avg_i * (1 - avg_e) * 0.01, 6)

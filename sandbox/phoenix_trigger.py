"""Phoenix Trigger — phase machine driven by Schumann pulse + plasma entropy."""
import time
import math
import json
from dataclasses import dataclass
from typing import Literal
from .plasma_usb_reader import PlasmaReading

Phase = Literal["SEEDING", "ASH", "UNFOLDING", "BLOOM"]


@dataclass
class PhoenixState:
    phase: Phase
    coherence: float
    rebirth_count: int
    last_event: str
    fold_verified: bool


class PhoenixTrigger:
    def __init__(self, config_path="config/live_constants.json"):
        with open(config_path) as f:
            cfg = json.load(f)
        self.target = cfg["lattice"]["target_coherence"]
        self.schumann = cfg["lattice"]["schumann_hz"]
        self.ash_thresh = cfg["plasma"]["ash_threshold"]
        self.bloom_thresh = cfg["plasma"]["bloom_threshold"]
        self.state = PhoenixState("SEEDING", 0.95, 0, "INIT", True)
        self.entropy_window: list[float] = []

    def update(self, plasma: PlasmaReading, contrib: float) -> PhoenixState:
        self.entropy_window.append(plasma.entropy)
        if len(self.entropy_window) > 15:
            self.entropy_window.pop(0)

        avg_e = sum(self.entropy_window) / len(self.entropy_window)
        pulse = math.sin(time.time() * self.schumann * 0.01)

        if avg_e >= self.ash_thresh and self.state.phase != "ASH":
            self.state.phase = "ASH"
            self.state.coherence = max(0.5, self.state.coherence - 0.12)
            self.state.last_event = f"ASH entropy={avg_e:.2f}"
        elif avg_e <= self.bloom_thresh and self.state.coherence < self.target:
            rise = 0.0015 * (1 - avg_e) * (1 + pulse * 0.5) + contrib
            self.state.coherence = min(1.0, self.state.coherence + rise)
            if self.state.coherence >= self.target:
                self.state.phase = "BLOOM"
                self.state.rebirth_count += 1
                self.state.last_event = f"REBIRTH #{self.state.rebirth_count}"
            elif self.state.phase == "ASH":
                self.state.phase = "UNFOLDING"

        return self.state

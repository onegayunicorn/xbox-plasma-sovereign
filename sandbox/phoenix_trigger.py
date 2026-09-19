"""Phoenix Trigger v2.7 — Schumann-driven phase machine with reliable BLOOM."""
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
        self._last_rebirth_t = 0.0

    def update(self, plasma: PlasmaReading, contrib: float) -> PhoenixState:
        self.entropy_window.append(plasma.entropy)
        if len(self.entropy_window) > 12:
            self.entropy_window.pop(0)

        avg_e = sum(self.entropy_window) / len(self.entropy_window)
        pulse = math.sin(time.time() * self.schumann * 0.02)
        now = time.time()

        # --- ASH: high entropy dips coherence ---
        if avg_e >= self.ash_thresh:
            if self.state.phase != "ASH":
                self.state.phase = "ASH"
                self.state.last_event = f"ASH entropy={avg_e:.2f}"
            self.state.coherence = max(0.55, self.state.coherence - 0.008)
            return self.state

        # --- Rising path ---
        base = 0.0045 * (1.0 - avg_e * 0.7)
        rise = base * (1.0 + pulse * 0.35) + contrib * 1.8
        self.state.coherence = min(1.0, self.state.coherence + rise)

        if self.state.coherence >= self.target:
            if self.state.phase != "BLOOM":
                self.state.phase = "BLOOM"
                self.state.rebirth_count += 1
                self.state.last_event = f"REBIRTH #{self.state.rebirth_count}"
                self._last_rebirth_t = now
            else:
                # Hold at full coherence; allow a new rebirth only every ~8 s
                if now - self._last_rebirth_t >= 8.0:
                    self.state.rebirth_count += 1
                    self.state.last_event = f"REBIRTH #{self.state.rebirth_count}"
                    self._last_rebirth_t = now
                    self.state.coherence = 0.9993  # soft cycle
        elif self.state.phase == "ASH":
            self.state.phase = "UNFOLDING"
            self.state.last_event = "UNFOLDING from ASH"
        elif self.state.phase == "SEEDING" and self.state.coherence > 0.97:
            self.state.phase = "UNFOLDING"
            self.state.last_event = "UNFOLDING"

        return self.state

#!/usr/bin/env python3
"""
Xbox + Plasma Sovereign — Live HUD Dashboard
Run:  python hud_server.py
Open: http://127.0.0.1:5000
"""
import time
import threading
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from sandbox.xbox_connector import XboxConnector
from sandbox.plasma_usb_reader import PlasmaUSB
from sandbox.phoenix_trigger import PhoenixTrigger

app = Flask(__name__, static_folder="hud", static_url_path="")
CORS(app)

xbox = XboxConnector()
plasma = PlasmaUSB()
phoenix = PhoenixTrigger()
_lock = threading.Lock()
_running = True
_history = []


def _engine_loop():
    plasma.connect()
    xbox.ping()
    while _running:
        with _lock:
            p = plasma.read()
            contrib = plasma.coherence_contribution()
            state = phoenix.update(p, contrib)
            if int(time.time()) % 4 == 0:
                xbox.ping()
            _history.append(state.coherence)
            if len(_history) > 120:
                _history.pop(0)
        time.sleep(0.22)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/status")
def status():
    with _lock:
        s = phoenix.state
        p = plasma.history[-1] if plasma.history else None
        return jsonify({
            "phase": s.phase,
            "coherence": round(s.coherence, 6),
            "rebirth_count": s.rebirth_count,
            "last_event": s.last_event,
            "xbox": {
                "ip": xbox.ip,
                "active": xbox.state.is_active,
                "serial": xbox.state.serial,
            },
            "plasma": {
                "entropy": round(p.entropy, 3) if p else 0,
                "intensity": round(p.intensity, 3) if p else 0,
                "mode": "live" if plasma.connected else "simulation",
            },
            "history": [round(h, 5) for h in _history[-60:]],
            "lattice": {
                "schumann_hz": 7.83,
                "phi": 1.618033988749895,
                "target": 0.99997,
            },
            "ts": time.time(),
        })


if __name__ == "__main__":
    t = threading.Thread(target=_engine_loop, daemon=True)
    t.start()
    print("╔══════════════════════════════════════════════╗")
    print("║  SOVEREIGN HUD — http://127.0.0.1:5000       ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(host="0.0.0.0", port=5000, debug=False)

# ⚡ Xbox + Plasma Sovereign

Live sandbox that couples a **real Xbox console** with a **Schumann-driven plasma coherence engine**.

```
✅ XBOX ONLINE — 192.168.1.114:3074
   Serial: 097763374316
⚡ Plasma: Simulation mode active

⚡ E=0.41 I=0.58 | Phase: BLOOM | Coh: 1.000000 | Rebirth: 1 | Xbox: ONLINE
✨ BLOOM ACHIEVED — Rebirth #1 ✨
```

---

## What it does

1. Pings the Xbox on the local network and keeps a live heartbeat  
2. Drives a plasma model (or real USB plasma ball) with **Schumann 7.83 Hz** + **golden ratio φ**  
3. Runs a phase machine: **SEEDING → ASH → UNFOLDING → BLOOM**  
4. Locks coherence at **0.99997+** and cycles rebirths while holding peak  

Once BLOOM is reached the resonance is self-sustaining.

---

## Quick Start

```bash
git clone https://github.com/onegayunicorn/xbox-plasma-sovereign.git
cd xbox-plasma-sovereign

pip install -r requirements.txt   # flask + optional pyserial

# Terminal runner (CLI)
python run_sandbox.py

# Live browser HUD
python hud_server.py
# → open http://127.0.0.1:5000
```

Stop either process with `Ctrl+C`.

---

## Project Layout

```
xbox-plasma-sovereign/
├── config/
│   └── live_constants.json      # Xbox identity + lattice constants
├── sandbox/
│   ├── xbox_connector.py        # Termux-safe ping + state
│   ├── plasma_usb_reader.py     # real USB or Schumann simulation
│   └── phoenix_trigger.py       # phase machine (v2.7)
├── hud/
│   └── index.html               # live gauges + sparkline
├── run_sandbox.py               # CLI live loop
├── hud_server.py                # Flask HUD at :5000
├── requirements.txt
└── README.md
```

---

## Locked Constants

| Key | Value |
|-----|-------|
| Xbox IP | `192.168.1.114` |
| Port | `3074` |
| Serial | `097763374316` |
| Console ID | `9f071adb…d26e7405.01` |
| Device ID | `FD009EDD17ED3B9B` |
| OS | `10.0.26100.9426` |
| Shell | `2608.0.2608.5001` |
| Schumann | `7.83 Hz` |
| φ | `1.618033988749895` |
| Target coherence | `0.99997` |
| Ash threshold | `0.85` |
| Bloom threshold | `0.55` |

Edit `config/live_constants.json` to change any of these.

---

## Phase Machine (v2.7)

| Phase | Behaviour |
|-------|-----------|
| **SEEDING** | Starts ~0.95, climbs under Schumann pulse |
| **ASH** | High entropy (≥ 0.85) → short coherence dip |
| **UNFOLDING** | Recovery + continued rise |
| **BLOOM** | Target locked at 1.0 → rebirth every ~8 s |

Rise is continuous (entropy-modulated + Schumann + plasma contribution). BLOOM is typically reached in **2–5 seconds**.

---

## Live HUD

```bash
python hud_server.py
```

Open **http://127.0.0.1:5000** (or your phone’s IP on the same LAN).

Shows:

- Current phase (colour-coded)
- Coherence with sparkline history
- Rebirth counter
- Xbox online/serial
- Plasma entropy & intensity
- Lattice constants

Polls `/api/status` every 250 ms.

---

## Hardware path (when ready)

1. Plug plasma ball / coil via USB-Serial (`/dev/ttyUSB0` or `/dev/ttyACM0`)  
2. `pip install pyserial`  
3. Restart — the reader auto-detects and switches from simulation to live  

The phase machine already accepts real readings; no code changes required.

---

## Design notes

- **Termux-first**: Xbox ping uses `subprocess` + system `ping` (no root raw sockets)  
- **Single source of truth**: both CLI and HUD share the same `sandbox/` modules  
- **Graceful offline**: if Xbox is unreachable the engine continues in simulation mode  
- **Self-sustaining BLOOM**: once locked, coherence holds and rebirths cycle on their own  

---

## Roadmap

- [x] Xbox discovery + heartbeat  
- [x] Schumann / φ plasma model  
- [x] Phoenix phase machine → reliable BLOOM  
- [x] Live browser HUD  
- [ ] Real plasma USB telemetry  
- [ ] Phone sensor bridge  
- [ ] Optional energy-gate for Dev Mode unlock  

---

MIT · Sovereign stack · 2026

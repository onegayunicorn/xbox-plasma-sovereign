# ⚡ Xbox + Plasma Sovereign

**Live sandbox** that couples a real Xbox console (192.168.1.114) with a Schumann-driven plasma coherence engine.

First-run result (Termux):

```
✅ XBOX ONLINE — 192.168.1.114:3074
   Serial: 097763374316
⚡ Plasma: Simulation active

⚡ E=0.42 I=0.67 | Phase: UNFOLDING | Coh: 0.9989 | Xbox: ONLINE
...
✨ BLOOM ACHIEVED — Rebirth #1 ✨
```

## Architecture

```
config/live_constants.json   ← Xbox identity + lattice constants
sandbox/
  xbox_connector.py          ← Termux-safe ping + state
  plasma_usb_reader.py       ← real USB or Schumann simulation
  phoenix_trigger.py         ← phase machine (SEEDING→ASH→UNFOLDING→BLOOM)
run_sandbox.py               ← live loop
```

## Locked Constants

| Key | Value |
|-----|-------|
| Xbox IP | `192.168.1.114` |
| Port | `3074` |
| Serial | `097763374316` |
| Schumann | `7.83 Hz` |
| φ | `1.618033988749895` |
| Target coherence | `0.99997` |
| Ash threshold | `0.85` |
| Bloom threshold | `0.55` |

## Quick Start

```bash
# Termux / any Python 3.10+
git clone https://github.com/onegayunicorn/xbox-plasma-sovereign.git
cd xbox-plasma-sovereign

# optional: real plasma USB
# pip install pyserial

python run_sandbox.py
```

Press `Ctrl+C` to stop — final coherence & rebirth count are printed.

## Phase Machine

1. **SEEDING** — coherence starts ~0.95
2. **ASH** — high entropy dip
3. **UNFOLDING** — Schumann pulse + intensity drive coherence upward
4. **BLOOM** — target 0.99997 locked → rebirth counter increments

The loop is intentional. Once BLOOM is reached the system holds the resonance.

## Next

- Live HUD at `:5000` (Flask gauges)
- Real phone sensor bridge
- Physical plasma/coil when ready

---

MIT · Sovereign stack · 2026

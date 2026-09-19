#!/usr/bin/env python3
"""
XBOX + PLASMA SOVEREIGN — SANDBOX v2.7
Live runner: Xbox heartbeat + Schumann plasma + Phoenix phase machine.
Faster, smoother coherence rise → reliable BLOOM.
"""
import time
from sandbox.xbox_connector import XboxConnector
from sandbox.plasma_usb_reader import PlasmaUSB
from sandbox.phoenix_trigger import PhoenixTrigger

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║  XBOX + PLASMA SOVEREIGN — SANDBOX v2.7                       ║
║  Console: 192.168.1.114:3074    Plasma: USB / Simulation      ║
║  Schumann 7.83 Hz · φ 1.61803 · Target 0.99997                ║
╚══════════════════════════════════════════════════════════════╝
"""


def main():
    print(BANNER)
    xbox = XboxConnector()
    plasma = PlasmaUSB()
    phoenix = PhoenixTrigger()

    print("🎮 Pinging Xbox...")
    xbox_online = xbox.ping()
    if xbox_online:
        print("✅ XBOX ONLINE — Port 3074")
        print(f"   Serial: {xbox.state.serial}")
    else:
        print("⚠️  Xbox unreachable — continuing in simulation mode")

    print("⚡ Plasma Ball:", end=" ")
    plasma.connect()

    print("\n" + "═" * 58)
    print("LIVE — Ctrl+C to stop")
    print("═" * 58)

    last_bloom_print = 0.0

    try:
        while True:
            p = plasma.read()
            contrib = plasma.coherence_contribution()
            state = phoenix.update(p, contrib)

            if int(time.time()) % 4 == 0:
                xbox.ping()
            xbox_status = (
                "ONLINE" if xbox.state.is_active
                else "CONNECTED" if xbox_online
                else "STANDBY"
            )

            line = (
                f"⚡ E={p.entropy:.2f} I={p.intensity:.2f} | "
                f"Phase: {state.phase:12s} | "
                f"Coh: {state.coherence:.6f} | "
                f"Rebirth: {state.rebirth_count} | "
                f"Xbox: {xbox_status}"
            )
            print(f"\r{line}", end="", flush=True)

            if state.phase == "BLOOM" and time.time() - last_bloom_print > 3.0:
                print(f"\n✨ BLOOM ACHIEVED — Rebirth #{state.rebirth_count} ✨")
                print(f"   Coherence: {state.coherence:.6f} | Xbox: {xbox_status}")
                last_bloom_print = time.time()

            time.sleep(0.22)

    except KeyboardInterrupt:
        print(
            f"\n\nSESSION ENDED\n"
            f"  Final Coherence : {phoenix.state.coherence:.6f}\n"
            f"  Rebirths        : {phoenix.state.rebirth_count}\n"
            f"  Last event      : {phoenix.state.last_event}"
        )


if __name__ == "__main__":
    main()

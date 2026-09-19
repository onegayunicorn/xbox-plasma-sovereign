#!/usr/bin/env python3
"""
XBOX + PLASMA SOVEREIGN — SANDBOX v2.6
Live runner: Xbox heartbeat + Schumann plasma + Phoenix phase machine.
"""
import time
from sandbox.xbox_connector import XboxConnector
from sandbox.plasma_usb_reader import PlasmaUSB
from sandbox.phoenix_trigger import PhoenixTrigger

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║  XBOX + PLASMA SOVEREIGN — SANDBOX v2.6                       ║
║  Console: 192.168.1.114:3074    Plasma: USB Live               ║
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
        print("⚠️  Xbox unreachable — continuing in simulation mode\n")

    print("⚡ Plasma Ball:", end=" ")
    plasma.connect()

    print("\n" + "═" * 50)
    print("LIVE — Ctrl+C to stop")
    print("═" * 50)

    try:
        while True:
            p = plasma.read()
            contrib = plasma.coherence_contribution()
            state = phoenix.update(p, contrib)

            if int(time.time()) % 5 == 0:
                xbox.ping()
            xbox_status = (
                "ONLINE"
                if xbox.state.is_active
                else "CONNECTED"
                if xbox_online
                else "STANDBY"
            )

            print(
                f"\r⚡ E={p.entropy:.2f} I={p.intensity:.2f} | "
                f"Phase: {state.phase:12s} | Coh: {state.coherence:.6f} | "
                f"Rebirth: {state.rebirth_count} | Xbox: {xbox_status}",
                end="",
                flush=True,
            )

            if state.coherence >= phoenix.target and state.phase == "BLOOM":
                print("\n✨ BLOOM ACHIEVED ✨")
                print(
                    f"   Rebirths: {state.rebirth_count} | "
                    f"Coherence: {state.coherence:.6f}"
                )
                time.sleep(2)

            time.sleep(0.25)

    except KeyboardInterrupt:
        print(
            f"\n\nSESSION ENDED | "
            f"Coherence: {phoenix.state.coherence:.6f} | "
            f"Rebirths: {phoenix.state.rebirth_count}"
        )


if __name__ == "__main__":
    main()

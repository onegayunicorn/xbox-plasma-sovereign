import socket, time, json, subprocess
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class XboxState:
    ip: str; port: int; serial: str; device_id: str
    os_version: str; shell_version: str; is_active: bool; last_seen: float

class XboxConnector:
    def __init__(self, config_path="config/live_constants.json"):
        with open(config_path) as f: cfg = json.load(f)["xbox"]
        self.ip, self.port = cfg["ip"], cfg["port"]
        self.state = XboxState(self.ip, self.port, cfg["serial"], cfg["device_id"],
            cfg["os_version"], cfg["shell_version"], False, 0)
    def ping(self) -> bool:
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", self.ip],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            ok = result.returncode == 0
            self.state.is_active = ok
            self.state.last_seen = time.time()
            return ok
        except: return False
    def get_summary(self) -> Dict:
        return {"ip": self.ip, "active": self.state.is_active, "serial": self.state.serial}

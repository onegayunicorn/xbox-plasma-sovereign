import socket, time, json
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
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5)
                ok = s.connect_ex((self.ip, self.port)) == 0
                self.state.is_active = ok; self.state.last_seen = time.time()
                return ok
        except: return False
    def get_summary(self) -> Dict:
        return {"ip": self.ip, "active": self.state.is_active, "serial": self.state.serial}

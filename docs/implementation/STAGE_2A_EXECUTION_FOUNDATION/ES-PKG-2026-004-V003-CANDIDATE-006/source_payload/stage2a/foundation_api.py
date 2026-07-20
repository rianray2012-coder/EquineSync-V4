#!/usr/bin/env python3
"""Loopback-only Stage 2A foundation API; exposes health only."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from lib.control import digest, load_env, mongo_client, validate_env

ENV = load_env()
POSTURE = validate_env(ENV)
CLIENT = mongo_client(ENV)
FINGERPRINT = digest({k: ENV[k] for k in sorted(ENV) if k not in {"PATH", "TMPDIR", "LANG", "LC_ALL", "PYTHONPATH"}})


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict[str, object]) -> None:
        raw = json.dumps(body, sort_keys=True).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health/live":
            return self._send(200, {"status": "alive", "profile": "stage2a-foundation"})
        if self.path == "/health/ready":
            try:
                CLIENT.admin.command("ping")
                return self._send(200, {"status": "ready", "datastore": POSTURE["datastore"], "configuration_fingerprint": FINGERPRINT, "business_routes": 0})
            except Exception:
                return self._send(503, {"status": "not_ready"})
        return self._send(404, {"status": "not_found"})

    def log_message(self, fmt, *args):
        print("foundation-api", fmt % args, flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer((ENV["STAGE2A_API_HOST"], int(ENV["STAGE2A_API_PORT"])), Handler)
    print(json.dumps({"event": "foundation_api_started", "host": ENV["STAGE2A_API_HOST"], "port": int(ENV["STAGE2A_API_PORT"]), "fingerprint": FINGERPRINT}, sort_keys=True), flush=True)
    try: server.serve_forever()
    finally:
        CLIENT.close(); server.server_close()

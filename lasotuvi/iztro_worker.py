"""Private JSON-lines worker that owns the PythonMonkey runtime."""

from __future__ import annotations

import json
import sys
from typing import Any


def _write(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def main() -> int:
    try:
        from py_iztro import Astro

        astro = Astro()
    except Exception as exc:
        _write({"id": None, "ok": False, "kind": "unavailable", "detail": str(exc)})
        return 1

    _write({"id": None, "ok": True, "payload": "ready"})
    for line in sys.stdin:
        request: dict[str, Any] = {}
        try:
            raw_request = json.loads(line)
            if not isinstance(raw_request, dict):
                raise ValueError("worker request must be an object")
            request = raw_request
            if request.get("command") == "shutdown":
                return 0
            method = astro.by_solar if request["is_solar"] else astro.by_lunar
            result = method(
                request["date"],
                request["time_index"],
                request["gender"],
                language="vi-VN",
            )
            _write(
                {
                    "id": request["id"],
                    "ok": True,
                    "payload": result.model_dump(by_alias=True),
                }
            )
        except ValueError as exc:
            _write(
                {
                    "id": request.get("id"),
                    "ok": False,
                    "kind": "value",
                    "detail": str(exc),
                }
            )
        except Exception as exc:
            _write(
                {
                    "id": request.get("id"),
                    "ok": False,
                    "kind": "runtime",
                    "detail": str(exc),
                }
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

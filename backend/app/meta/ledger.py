"""Append-only cost ledger for every Meta Model API call, with a hard budget guard and a per-run event hook."""
from __future__ import annotations

import json
import threading
import time
from collections import defaultdict
from typing import Callable

from ..config import BUDGET_USD, PRICE, VAR

LEDGER = VAR / "ledger.jsonl"
_lock = threading.Lock()
_spent = 0.0
_listeners: list[Callable[[dict], None]] = []


class BudgetExceeded(RuntimeError):
    pass


def _load() -> None:
    global _spent
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                _spent += json.loads(line).get("cost_usd", 0.0)
            except json.JSONDecodeError:
                pass


_load()


def on_call(fn: Callable[[dict], None]) -> None:
    _listeners.append(fn)


def spent() -> float:
    return round(_spent, 4)


def check_budget(expected: float = 0.0) -> None:
    if _spent + expected > BUDGET_USD:
        raise BudgetExceeded(f"Meta API budget guard: spent ${_spent:.2f} of ${BUDGET_USD:.2f}")


def spark_cost(model: str, prompt_tokens: int, completion_tokens: int, cached: int) -> float:
    p = PRICE.get(model, PRICE["muse-spark-1.3"])
    return (prompt_tokens - cached) * p["in"] + cached * p["cached"] + completion_tokens * p["out"]


def record(model: str, op: str, ms: float, status, cost_usd: float, run_id: str | None = None, **extra) -> dict:
    global _spent
    rec = {"t": round(time.time(), 3), "model": model, "op": op, "ms": round(ms), "status": status,
           "cost_usd": round(cost_usd, 6), "run_id": run_id, **extra}
    with _lock:
        _spent += cost_usd
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    for fn in _listeners:
        try:
            fn(rec)
        except Exception:
            pass
    return rec


def recent(limit: int = 200) -> list[dict]:
    if not LEDGER.exists():
        return []
    lines = LEDGER.read_text(encoding="utf-8").splitlines()[-limit:]
    return [json.loads(x) for x in lines if x.strip()]


def by_model() -> dict:
    agg: dict = defaultdict(lambda: {"calls": 0, "cost_usd": 0.0})
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            agg[r["model"]]["calls"] += 1
            agg[r["model"]]["cost_usd"] = round(agg[r["model"]]["cost_usd"] + r.get("cost_usd", 0), 4)
    return dict(agg)

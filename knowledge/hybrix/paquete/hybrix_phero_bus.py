#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bus de feromonas in-memory para HYBRIX (estigmergia L5).

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA
Licencia: MIT
"""

from __future__ import annotations

import threading
import time
from typing import Any, Dict, Optional


class PheromoneBus:
    """
    Bus simple de feromonas con TTL.
    Interfaz: deposit(clave, valor, ttl_s) / sniff(clave) -> valor o None.
    Pensado para simulación local y tests; no es un bus LoRa real.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._store: Dict[str, Dict[str, Any]] = {}

    def deposit(self, key: str, value: Any, ttl_s: float = 300.0) -> None:
        expires_at = time.monotonic() + float(ttl_s) if ttl_s and ttl_s > 0 else None
        with self._lock:
            self._store[key] = {"value": value, "expires_at": expires_at, "deposited_at": time.time()}

    def sniff(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at = entry.get("expires_at")
            if expires_at is not None and time.monotonic() > expires_at:
                del self._store[key]
                return None
            return entry.get("value")

    def clear(self, key: Optional[str] = None) -> None:
        with self._lock:
            if key is None:
                self._store.clear()
            else:
                self._store.pop(key, None)

    def keys(self) -> list:
        with self._lock:
            now = time.monotonic()
            alive = []
            expired = []
            for k, entry in self._store.items():
                expires_at = entry.get("expires_at")
                if expires_at is not None and now > expires_at:
                    expired.append(k)
                else:
                    alive.append(k)
            for k in expired:
                del self._store[k]
            return list(alive)

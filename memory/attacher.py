"""Thin wrapper around pymem that exposes typed read/write helpers."""
from __future__ import annotations

import logging

import pymem

log = logging.getLogger(__name__)


class ProcessAttacher:
    def __init__(self, process_name: str, backend: str = "pymem") -> None:
        self.process_name = process_name
        self.backend = backend
        self._pm: pymem.Pymem | None = None

    def attach(self) -> bool:
        try:
            self._pm = pymem.Pymem(self.process_name)
            log.info("attached to %s (pid=%d)", self.process_name, self._pm.process_id)
            return True
        except pymem.exception.ProcessNotFound:
            return False

    def detach(self) -> None:
        self._pm = None

    def base_address(self, module: str) -> int:
        return pymem.process.module_from_name(self._pm.process_handle, module).lpBaseOfDll

    def read_float(self, addr: int) -> float:
        return pymem.memory.read_float(self._pm.process_handle, addr)

    def write_float(self, addr: int, value: float) -> None:
        pymem.memory.write_float(self._pm.process_handle, addr, value)

    def write_byte(self, addr: int, value: int) -> None:
        pymem.memory.write_char(self._pm.process_handle, addr, chr(value))

    def read_pointer(self, addr: int) -> int:
        return pymem.memory.read_ulonglong(self._pm.process_handle, addr)

    def read_fstring(self, addr: int, max_len: int = 64) -> str:
        raw = pymem.memory.read_bytes(self._pm.process_handle, addr, max_len)
        return raw.split(b"\x00", 1)[0].decode("utf-8", errors="ignore")
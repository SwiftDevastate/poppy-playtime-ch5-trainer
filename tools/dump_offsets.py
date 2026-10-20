"""Helper: hash a running Chapter 5 module and dump candidate offsets to offsets/dump.json."""
from __future__ import annotations

import hashlib
import json
import sys

import pymem
import pymem.process


def main(proc: str = "PoppyPlaytime_Ch5.exe") -> int:
    pm = pymem.Pymem(proc)
    mod = pymem.process.module_from_name(pm.process_handle, "PoppyPlaytime_Ch5-Win64-Shipping.exe")
    data = pymem.memory.read_bytes(pm.process_handle, mod.lpBaseOfDll, mod.SizeOfImage)
    digest = hashlib.sha256(data).hexdigest()
    out = {"module_size": mod.SizeOfImage, "sha256": digest, "base": hex(mod.lpBaseOfDll)}
    with open("offsets/dump.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("dumped", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
</<dyad_completion>>
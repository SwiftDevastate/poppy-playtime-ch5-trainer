# Security Policy

## Scope
This repository is an external, user-mode trainer for **Poppy Playtime - Chapter 5**.
It reads/writes process memory of the local game client only. No network cheating,
no anti-cheat bypass for online services (Chapter 5 is single-player).

## Reporting a vulnerability
If you find an issue in the **trainer itself** (e.g. arbitrary code exec via a
malicious config file, DLL hijack in `backends/`), open a private security advisory
or email `security@ppch5-trainer.dev` with PGP.

## What we will NOT accept
- Requests to add anti-cheat bypasses targeting third-party online games.
- Instructions to weaponize the loader for unrelated processes.

## Known limitations
- The `backends/injector` module requires the game to be launched with
  `-nolauncher` for stable attach.
- Configs are YAML-parsed with `yaml.safe_load` only; do not add `!!python/object`
  tags.
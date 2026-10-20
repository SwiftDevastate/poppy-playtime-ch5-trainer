# Contributing to poppy-playtime-ch5-trainer

Thanks for wanting to help out with the Chapter 5 trainer!

## Ground rules
- Read `SECURITY.md` before touching the memory / injection layers.
- All new features must be togglable from `config/default.yaml`.
- Keep the overlay render loop under 2 ms; the game's timer (PoE minigame) is sensitive to stalls.

## Pull request flow
1. Fork + branch from `main` (`feat/<feature>` or `fix/<bug>`).
2. Run `python -m pytest tests/` locally — CI runs the same on Windows 2022 runners.
3. Update `offsets/signatures.py` if you're adding a new pattern.
4. Describe which game process build you tested against (e.g. `PP_Ch5 v1.0.3.114`).

## Coding style
- Python 3.10+, `black` + `ruff`.
- Feature modules live in `trainer_core/features/`. Shared logic belongs in `trainer_core/lib/`.
- Never hard-code a raw pointer; always resolve via the `memory.offsets` resolver.

## Reporting offsets
Game updates will break signatures — open an issue titled `offset-drift: <module>` and include a minidump hash.
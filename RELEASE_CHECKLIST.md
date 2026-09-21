# AutoClip EN

> EN：**EN**，EN（`1.3.0 → 1.4.0 → …`，EN `x.y.1`）。
> EN「EN」，EN「EN main EN」。`HANDOFF.md` EN v1.3 / v1.4 EN。
> EN（EN tag EN Release EN）EN 25 EN，EN `desktop-build.yml` EN；EN。

## EN（EN – EN）

- [ ] EN **CI EN + EN** EN PR（PR EN「EN」）。EN PR EN `HANDOFF.md` EN。
- [ ] EN PR EN `CHANGELOG.md` EN `## [EN]` EN（EN / EN / EN），EN，EN。
- [ ] EN **EN** EN **EN**（issue EN）。
- [ ] EN（`scripts/weekly_digest.py`）EN，EN，EN `HANDOFF.md` EN。

## EN（EN / EN，EN 24 EN）

- [ ] main CI EN（`gh run list --branch main --limit 1`）。
- [ ] `python scripts/bump_version.py --check` EN。
- [ ] EN `pytest backend/tests`、`cd frontend && npm run lint && npm run typecheck && npm run build`、`python -m backend.eval`。
- [ ] EN `CHANGELOG.md [EN]`：EN、EN issue EN PR、EN / EN。
- [ ] `python scripts/bump_version.py X.Y.0 --commit`
      → EN `tauri.conf.json` / `Cargo.toml` / `pyproject.toml` / `desktop_config.py`，EN `[EN]` EN `[X.Y.0] - EN`。
- [ ] `git push origin main && git tag vX.Y.0 && git push origin vX.Y.0`
      → EN `desktop-build.yml`：macOS arm64 DMG + Windows x64 EN，`release` job EN `scripts/release_notes.py`
      EN CHANGELOG EN + EN Release EN。
- [ ] EN Actions EN Desktop Build EN、Release EN（EN = EN，EN run EN）。

## EN（EN）

- [ ] **EN（EN，CI EN）**：
  - Windows：EN `-setup.exe` → EN → EN provider → EN。**Windows EN DMG EN 3 EN，EN。**
  - macOS：EN DMG EN → EN。
- [ ] EN #96 EN「v1.x EN」EN。
- [ ] EN Release EN `needs-info` / EN issue：EN（EN `HANDOFF.md` EN）。
- [ ] `HANDOFF.md` EN「EN：EN · main@sha」EN。

## EN（EN bug）

- [ ] EN → PR → CI EN → EN → `bump_version.py X.Y.1 --commit` → EN tag。EN。

## EN

- EN；EN CI / EN CHANGELOG EN。
- EN（EN），EN Release EN（EN CHANGELOG EN）。
- EN「EN」EN。main EN。

## EN

| EN | EN |
|---|---|
| EN + CHANGELOG EN | `scripts/bump_version.py` |
| Release EN | `scripts/release_notes.py`（EN `desktop-build.yml` EN `release` job EN） |
| EN workflow | `.github/workflows/desktop-build.yml`（tag `v*` EN；`workflow_dispatch` EN） |
| EN | `scripts/build_macos_arm.sh`、`scripts/build_windows_x64.sh`（EN `BUILD_GUIDE.md`、`scripts/README.md`） |
| EN | `scripts/weekly_digest.py` |
| EN / EN | `HANDOFF.md` |

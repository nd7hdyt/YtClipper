# AutoClip 

> ：**Monday**，version（`1.3.0 → 1.4.0 → …`， `x.y.1`）。
> target「」，「 main verify」。`HANDOFF.md`  v1.3 / v1.4 。
> （ tag  Release ） 25 minutes， `desktop-build.yml` completed；。

## （Monday – Friday）

- [ ]  **CI  + verify**  PR（PR 「」）。 PR  `HANDOFF.md` 。
- [ ]  PR  `CHANGELOG.md`  `## []` （added / fix / improve），，。
- [ ]  **failed**  **install**（issue ）。
- [ ] （`scripts/weekly_digest.py`）issue，， `HANDOFF.md` 。

## （ / ， 24 ）

- [ ] main CI （`gh run list --branch main --limit 1`）。
- [ ] `python scripts/bump_version.py --check` version。
- [ ] local `pytest backend/tests`、`cd frontend && npm run lint && npm run typecheck && npm run build`、`python -m backend.eval`。
- [ ]  `CHANGELOG.md []`：、 issue  PR、 / key。
- [ ] `python scripts/bump_version.py X.Y.0 --commit`
      →  `tauri.conf.json` / `Cargo.toml` / `pyproject.toml` / `desktop_config.py`， `[]`  `[X.Y.0] - date`。
- [ ] `git push origin main && git tag vX.Y.0 && git push origin vX.Y.0`
      →  `desktop-build.yml`：macOS arm64 DMG + Windows x64 installbuild，`release` job  `scripts/release_notes.py`
       CHANGELOG version + notesgenerate Release 。
- [ ]  Actions  Desktop Build 、Release file（ = buildfailed， run ）。

## （）

- [ ] **verify（，CI ）**：
  - Windows： `-setup.exe` → start → Settings page provider → local。**Windows download DMG  3 ，。**
  - macOS：open DMG  → 。
- [ ] update #96 version「v1.x 」。
- [ ]  Release  `needs-info` / fix issue：（ `HANDOFF.md` ）。
- [ ] `HANDOFF.md` 「update：date · main@sha」status。

## （impact bug）

- [ ]  → PR → CI  →  → `bump_version.py X.Y.1 --commit` →  tag。weekend。

## 

- ； CI /  CHANGELOG 。
- editversion（）， Release （ CHANGELOG generate）。
- 「」。main 。

## file

|  | location |
|---|---|
| version + CHANGELOG  | `scripts/bump_version.py` |
| Release generate | `scripts/release_notes.py`（ `desktop-build.yml`  `release` job call） |
| build workflow | `.github/workflows/desktop-build.yml`（tag `v*` ；`workflow_dispatch` build） |
|  | `scripts/build_macos_arm.sh`、`scripts/build_windows_x64.sh`（notes `BUILD_GUIDE.md`、`scripts/README.md`） |
|  | `scripts/weekly_digest.py` |
| status /  | `HANDOFF.md` |

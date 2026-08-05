# Final release checklist — 2.3.0

## Release readiness

- [x] Confirm package metadata and version in pyproject.toml (2.3.0, GPL-3.0-only, SpinnCompany URLs)
- [x] Verify the test suite passes in a clean environment (1316 passed locally; public CI green on all four jobs: pytest 3.10 + 3.13, mypy, design-lint)
- [x] Build wheel and sdist artifacts (from the released tree — never ship a dist/ older than the tip)
- [x] Review README and install instructions for accuracy (extras documented; permanent-home note)
- [x] Verify changelog/release notes are ready (CHANGELOG.md, 2.3.0)
- [x] Confirm optional dependency groups are documented (qr / map / acrylic / acrylic-hq / loaders / mcp / dev / all; mcp pinned >=1.9,<2)
- [x] Inspect the artifacts: `twine check`, no internal docs (docs/design, docs/relicense), no premium examples, data files present (Qss, components, fonts)
- [x] Fresh-venv install smoke: import, instantiate a widget offscreen, CLI entry points resolve, missing-mcp import degrades to a clean message
- [ ] Upload to PyPI (`twine upload dist/*`) — the irreversible step
- [ ] Verify `pip install QT-PyQt-PySide-Custom-Widgets==2.3.0` from PyPI in a clean venv
- [ ] Tag `v2.3.0` on the public main and push the tag
- [ ] Then the Pro release: bump/confirm Pro version, run `wheels.yml` (workflow_dispatch or `v*` tag), upload the CI-built wheels (never a local build — bare `linux_x86_64` tags are rejected); Pro's LICENSE must be finalized first (still DRAFT)

## Verification commands

```bash
.venv/bin/python -m pytest tests/ -q      # 1316 passed
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
tar tzf dist/*.tar.gz | grep -cE 'docs/design|docs/relicense|AuroraChat|NodeStudio'   # must be 0
```

## Notes

- The sdist/wheel content comes from MANIFEST.in (`Custom_Widgets/**` only) +
  README/pyproject; the internal design docs and premium apps must never
  appear in an artifact — the grep above is the gate.
- The free wheel is pure Python (`py3-none-any`) so a local build is fine to
  upload; that is NOT true for Pro (compiled, cibuildwheel-only).

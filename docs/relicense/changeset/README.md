# Relicense changeset (GPLv3 → LGPLv3) — ready to execute

A self-contained, **ready-to-merge** kit that performs the GPLv3 → LGPLv3
relicense of the free core. It is staged here and **not yet applied** — the live
repo remains GPLv3 until you run it.

## ⚠️ Preconditions (do NOT run until all are true)

1. **Legal counsel has reviewed** the de-minimis assessment in
   `../external-contributions-audit.md` (and any contributor consents recorded in
   `../consent-tracking-issue.md`).
2. The **CLA** is finalized (counsel-reviewed §2 relicensing grant) and the CLA
   bot gates new PRs — so no new un-agreed GPL code lands during/after the flip.
3. `LICENSING.md` has been finalized (store links, contact, counsel review) and is
   ready to promote in the same change or immediately after.

## Contents

| File | Role |
|---|---|
| `COPYING.LESSER` | LGPLv3 text (canonical, from gnu.org) |
| `COPYING` | GPLv3 text (LGPL references it) |
| `LICENSE` | New root LICENSE notice (LGPLv3) |
| `RELICENSE-RECORD.md` | Record installed at repo root; fill in the date/consents |
| `apply_relicense.py` | The executor (dry-run by default) |

## How to run

From the repo root:

```bash
# 1. Preview — writes nothing, prints every planned change + SPDX file counts:
python docs/relicense/changeset/apply_relicense.py

# 2. Execute:
python docs/relicense/changeset/apply_relicense.py --apply

# 3. Review, test, commit:
git status && git diff --stat
python -m pytest -q            # sanity — no runtime behaviour changes expected
git add -A
git commit -m "Relicense free core to LGPLv3"   # single relicense commit
```

## What it changes

1. Installs `COPYING`, `COPYING.LESSER`, and the new `LICENSE` at the repo root.
2. Rewrites the two license lines in `pyproject.toml` (SPDX id + OSI classifier).
3. Adds `# SPDX-License-Identifier: LGPL-3.0-or-later` to **project-authored**
   Python under `Custom_Widgets/`, `tests/`, `examples/`.
   - **Skipped:** vendored/third-party (`Custom_Widgets/iconify/`,
     `AnalogGaugeWidget.py`, `ProgressIndicator.py`), machine-generated files
     (e.g. `ui_interface.py`), and anything already carrying an SPDX id. These
     keep their own licenses (see `Custom_Widgets/THIRD_PARTY_NOTICES.md`).
4. Writes `RELICENSE-RECORD.md` at the repo root.

The README license badge is dynamic and updates itself once GitHub detects LGPL
from `COPYING.LESSER`.

## After executing

- Promote `docs/design/LICENSING.draft.md` → `/LICENSING.md` and
  `docs/design/CONTRIBUTING.draft.md` → `/CONTRIBUTING.md` and
  `docs/design/CLA.draft.md` → `/CLA.md` (per their own checklists).
- Update the docs repo (Docusaurus) license references.
- Fill in `RELICENSE-RECORD.md` with the date and any consents, and attach
  counsel's sign-off.

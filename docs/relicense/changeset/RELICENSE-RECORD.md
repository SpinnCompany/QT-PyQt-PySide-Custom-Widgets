# Relicense record — GPLv3 → LGPLv3

**Date:** _<fill in on execution>_
**Prior license:** GNU General Public License v3.0 only (`GPL-3.0-only`)
**New license:** GNU Lesser General Public License v3.0 or later
(`LGPL-3.0-or-later`)

## Why

The free core is relicensed to **LGPLv3** to support the project's open-core
model: proprietary/commercial applications may use the free core freely, and the
separate commercial `custom-widgets-pro` add-on can link it. See
`docs/design/lgpl-relicense-plan.md` and `docs/design/LICENSING.md`.

## Authority to relicense

- The project owner (Khamisi Kibet / SpinnCompany, identities consolidated in
  `.mailmap`) authored **~98.6%** of commits and consents to the relicense.
- Every external contribution was audited by an authoritative full-tree
  `git blame` sweep (`docs/relicense/external-contributions-audit.md`): of five
  external contributors, three have **no surviving lines**; the remaining two
  have **11 lines total**, all package-dictated `import` statements or
  tool-generated boilerplate carrying **no protectable expression** (de minimis).
- _<Record here any explicit contributor consents obtained, with dates/links, and
  any lines regenerated or rewritten. Attach counsel's confirmation of the
  de-minimis assessment.>_

## What changed

- Added `COPYING.LESSER` (LGPLv3) and `COPYING` (GPLv3, referenced by the LGPL).
- Replaced the root `LICENSE` with an LGPLv3 notice.
- `pyproject.toml`: `license` → `LGPL-3.0-or-later`; OSI classifier → LGPLv3.
- Added `SPDX-License-Identifier: LGPL-3.0-or-later` headers to project-authored
  source (vendored/third-party and generated files were **not** stamped and keep
  their own licenses — see `Custom_Widgets/THIRD_PARTY_NOTICES.md`).
- The README license badge is dynamic and reflects the new license automatically.

## Not covered by this relicense

- **Qt** (PySide6 / PyQt6) — licensed separately by The Qt Company / Riverbank.
- The proprietary **`custom-widgets-pro`** add-on.
- Bundled third-party assets (icons/fonts) — their own licenses, in
  `Custom_Widgets/licenses/`.

# GPLv3 → LGPLv3 relicense plan + CLA rollout

**Status:** Groundwork done (2026-07-23) — `.mailmap` in place, external audit
complete; relicense execution is **counsel-gated** (see below).
**Owner:** TBD
**Created:** 2026-07-22
**Related:** commercial-product.md, LICENSING.draft.md, CLA.draft.md,
`docs/relicense/external-contributions-audit.md`,
`docs/relicense/consent-tracking-issue.md`

> **2026-07-23 update.** The external-contribution audit is done (see
> `docs/relicense/`). Owner is **~98.6%** (408/414 commits). Only **2 of 5**
> externals have any surviving lines, and those **11 lines total** are all
> package-dictated imports (youngsikshin, 8) or tool-generated example boilerplate
> (Théo Brunet, 3) — i.e. **no protectable expression**. The consent axis is
> effectively clear pending counsel's de-minimis confirmation. The remaining
> blockers are legal review + the actual license flip (mechanics below), not
> engineering.

> **Not legal advice.** This plan and the CLA draft must be reviewed by qualified
> counsel before execution. It describes a process, not a legal opinion.

## Why relicense

The commercial/open-core model (commercial-product.md) needs the free core under
**LGPLv3** so that:
- proprietary apps can use the free core freely (wider adoption), and
- the closed `custom-widgets-pro` package can legally link the core.

Relicensing from GPLv3 to LGPLv3 requires the consent of **all copyright holders**
in the work (each contributor owns copyright in their contribution; the maintainer
cannot unilaterally relicense others' code).

## Ownership baseline (favorable)

From `git shortlog -sne` (379 commits total):

- **Khamisi Kibet / SpinnCompany (project owner):** ~370 commits (~97.6%) across
  identities: `82152373+KhamisiKibet@…`, `kibetkhamisi@gmail.com`,
  `spinncompany@gmail.com`.
- **External contributors:** ~9 commits (~2.4%) from 5 identities.

**Action:** consolidate the owner's own identities in a `.mailmap` so authorship
is unambiguous, then clear the 5 externals below.

## External contribution audit

| Contributor | Commits | Touched | Nature | Assessment |
|---|---|---|---|---|
| Enigma Project `diosa.business@gmail.com` | 4 | `ProjectMaker.py`, `ui_interface.py`, `setup.py` | Deletions + setup.py fixes + comments | Deletions = no copyright interest; setup.py fixes likely de minimis |
| youngsikshin `bluevow@gmail.com` | 2 | `Custom_Widgets/__init__.py`, `QCustomQPushButton.py`, `iconify/*` | Windows support, import-path edits | Small functional fixes; rewritable |
| Théo Brunet `t-brunet@alphee-dev.fr` | 1 | `examples/QPushButtons/*` | Example fix (.ui + generated `ui_interface.py`) | Example/generated file; low/no threshold |
| boscs `swan.bosc@outlook.fr` | 1 | `examples/AnalogGaugeMeterWidget/…` | Example fix | Example file; rewritable |
| enigmapr0ject `leigh@enigmapr0ject.live` | 1 | `ProjectMaker.py`, `components/python/ui_interface.py` | Windows fix | Likely same entity as Enigma Project; small fix |

Observation: every external change is a **small, functional bug fix, an
example/auto-generated file, or a deletion.** Several are plausibly below the
threshold of copyrightability (functional/trivial), and all are easily rewritten
if consent can't be obtained. Legal counsel to confirm the de-minimis calls.

## Clearing process (per external contributor)

**Tier 1 — obtain consent (preferred).** Open a tracking GitHub issue and contact
each contributor (issue mention + email). Ask them to reply with the agreement
text below and, going forward, sign the CLA. A public reply on the issue is a
durable record.

> **Consent request template:**
> "Hi — Custom Widgets is relicensing its core library from GPLv3 to LGPLv3 to
> support a sustainable open-core model. You contributed the following commit(s):
> `<hashes>`. Do you agree to license your contribution(s) to the project under
> **LGPLv3** (and permit the project to distribute them under LGPLv3)? A simple
> reply 'I agree' on this issue is sufficient. Thank you!"

**Tier 2 — non-responsive or declining.** For any contributor who doesn't respond
within a reasonable window (e.g. 30 days) or declines:
1. Identify the exact surviving lines: `git log --author="<email>" -p` and
   `git blame` the touched files to see if their lines still exist.
2. If the change is **de minimis / purely functional** (import path, one-line
   Windows fix) — counsel may advise it carries no protectable expression.
3. Otherwise **revert or rewrite** the specific hunks (trivial here), then note it.

**Record everything** in `docs/relicense/` (or the tracking issue): who consented,
when, and what was rewritten.

## Relicense mechanics (once all holders cleared)

1. Add **`COPYING.LESSER`** (LGPLv3 text). Keep `COPYING`/GPLv3 as LGPL references
   the GPL text.
2. Replace root **`LICENSE`** with LGPLv3 (or a notice pointing to
   `COPYING.LESSER` + `COPYING`).
3. Update **`setup.py`**: `license="LGPLv3"` and classifier
   `License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)`.
4. Add **SPDX headers** to source files:
   `# SPDX-License-Identifier: LGPL-3.0-or-later`.
5. Update **README** license badge + any docs (and the separate Docusaurus repo).
6. Add a **`NOTICE`/relicense record** documenting the date, prior license, and
   contributor consents.
7. Single **"Relicense to LGPLv3"** commit (or tagged release) marking the change.
8. Promote **`LICENSING.draft.md` → `/LICENSING.md`** (per that doc's checklist).

## CLA rollout (for all future contributions)

Because the project **dual-licenses** (free LGPL core + commercial Pro), a plain
inbound=outbound or DCO is **not sufficient** — the maintainer needs the right to
license contributions under *other* terms (including proprietary). So:

1. Adopt the **Individual CLA** in `CLA.draft.md` (grants the maintainer a broad,
   irrevocable license incl. the right to sublicense/relicense). Add a
   **Corporate CLA** variant for company contributors.
2. Automate with a **CLA bot** (e.g. CLA Assistant) that blocks PR merge until the
   contributor signs. Store signatures in a repo/gist of record.
3. Add **`CONTRIBUTING.md`** explaining the CLA requirement and why (sustainability
   via the commercial Pro tier).
4. Optionally require **DCO sign-off** (`git commit -s`) in addition, for origin
   certification.

## Sequenced checklist

- [x] Add `.mailmap` consolidating owner identities — **done** (canonical
      `Khamisi Kibet <kibetkhamisi@gmail.com>`; 4 alias identities mapped)
- [x] `git blame` surviving external lines (Tier 2 fact-find) — **done**, see
      `docs/relicense/external-contributions-audit.md`: only 11 de-minimis lines
      survive (8 imports + 3 generated), 4/5 externals clear
- [x] Prepare relicense tracking issue + consent template — **ready to post**,
      `docs/relicense/consent-tracking-issue.md`
- [ ] (Optional, belt-and-suspenders) post the issue / email the 2 reachable
      survivors for explicit consent
- [ ] (Optional hard-clear) regenerate the one example `ui_interface.py`
      (Théo Brunet's 3 generated lines)
- [ ] **Legal review** of the de-minimis assessments + any consents — *gates the
      flip*
- [ ] Land CLA + CLA bot + `CONTRIBUTING.md` (gates new contributions) — drafts
      ready in `docs/design/`; counsel to review the §2 relicense grant first
- [ ] Execute relicense mechanics (COPYING.LESSER, LICENSE, `pyproject.toml`,
      SPDX headers, README) — **only after legal review**
- [ ] Record consents in `docs/relicense/`
- [ ] Promote `LICENSING.md`; announce the change

## Risk notes

- Consent is easiest **now** while the contributor set is tiny — every new GPL
  contributor without a CLA makes a future relicense harder. **Land the CLA + bot
  first** so the problem stops growing while you clear the existing five.
- Keep the owner-identity consolidation accurate; mis-attributing an owner commit
  as external creates phantom clearing work.

# Relicense consent — tracking issue (ready to post)

Draft text for a public GitHub tracking issue to record contributor consent for
the **GPLv3 → LGPLv3** relicense. Per the audit
(`external-contributions-audit.md`), only **2 of 5** external contributors have
any surviving lines, and those are de-minimis (package-dictated imports and
tool-generated boilerplate). Consent is therefore **belt-and-suspenders**, not
strictly required — but a public "I agree" is the cleanest durable record if the
contributors are reachable.

> Post this as an issue in the repo, `@`-mention each contributor, and (optionally)
> email them. Record replies here or in `external-contributions-audit.md`.

---

## Issue title

`Relicense: GPLv3 → LGPLv3 — contributor consent`

## Issue body

> **Custom Widgets is relicensing its free core from GPLv3 to LGPLv3** to support a
> sustainable open-core model (a free LGPL library plus a separately-licensed
> commercial add-on). The LGPL lets everyone — including closed-source and
> commercial apps — use the free core, while keeping the library itself open.
>
> Relicensing needs the agreement of everyone whose code is still in the tree. We
> audited every external contribution (`docs/relicense/external-contributions-audit.md`):
> most no longer have any surviving lines, and the few that remain are trivial
> (import statements / generated code). We'd still like your explicit OK on record.
>
> **If you are tagged below, please reply with "I agree".**
>
> ### Consent statement
> > I, the author of the commit(s) listed next to my name below, agree to license
> > my contribution(s) to the QT-PyQt-PySide-Custom-Widgets project under the
> > **GNU Lesser General Public License v3.0 (LGPLv3)**, and I permit the project
> > to distribute them under LGPLv3.
>
> ### Contributors & commits
> - @youngsikshin (`bluevow@gmail.com`) — `1851c3e` (modify import path),
>   `b59511a` (support win). Surviving: 8 import lines in `Custom_Widgets/iconify/`.
> - @theo-brunet (`t-brunet@alphee-dev.fr`) — `88e042c` (QPushButtons example fix).
>   Surviving: 3 generated lines in `examples/PySide6/QCustomQPushButton/ui_interface.py`.
> - @EnigmaProject (`diosa.business@gmail.com`) — `b540bdd`, `8499803`, `730c4c0`,
>   `0000934`. **No surviving lines** (deletions / removed `setup.py`).
> - @enigmapr0ject (`leigh@enigmapr0ject.live`) — `207f542` (Windows fix).
>   **No surviving lines.**
> - @boscs (`swan.bosc@outlook.fr`) — `97b6e7d` (example fix). **No surviving lines.**
>
> Going forward, contributions will be covered by the project's CLA (see
> `CONTRIBUTING.md`). Thank you!

## Direct-email variant (per the plan's template)

> Subject: Custom Widgets — relicensing your contribution to LGPLv3
>
> Hi — Custom Widgets is relicensing its core library from GPLv3 to LGPLv3 to
> support a sustainable open-core model. You contributed the following commit(s):
> `<hashes>`. Do you agree to license your contribution(s) to the project under
> **LGPLv3** (and permit the project to distribute them under LGPLv3)? A simple
> reply "I agree" is sufficient. Thank you!

---

## Consent log (fill in as replies arrive)

| Contributor | Consent | Date | Link / note |
|---|---|---|---|
| youngsikshin | — | — | 8 de-minimis import lines; consent optional |
| Théo Brunet | — | — | 3 generated lines; consent optional (or regenerate file) |
| Enigma Project | n/a | — | no surviving lines |
| enigmapr0ject | n/a | — | no surviving lines |
| boscs | n/a | — | no surviving lines |

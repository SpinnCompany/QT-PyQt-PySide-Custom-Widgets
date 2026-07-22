# Licensing

> **⚠️ DRAFT — NOT YET IN EFFECT.**
> This document describes the *target* licensing model for Custom Widgets. It
> takes effect only after two prerequisites are complete:
> 1. A Contributor License Agreement (CLA/DCO) is in place, and
> 2. The free core is relicensed **GPLv3 → LGPLv3**.
>
> **Until then, the free library remains licensed under GPLv3** (see the root
> `LICENSE` file). When the prerequisites are met, this file is promoted to
> `/LICENSING.md`.
>
> **This draft has not been reviewed by a lawyer.** It must be reviewed by
> qualified legal counsel before it governs any sale or distribution. Nothing
> here is legal advice.

---

## Overview — open-core

Custom Widgets uses an **open-core** model with two parts:

| Part | Package | License | Cost |
|---|---|---|---|
| **Free core** | `QT-PyQt-PySide-Custom-Widgets` | **LGPLv3** | Free, open source |
| **Pro add-on** | `custom-widgets-pro` | **Proprietary / commercial** | Paid (see below) |

The free core is fully functional and open source. The Pro add-on provides
production-grade widgets (starting with **DataTable Pro**) and requires a paid
entitlement to **develop with**.

---

## 1. The free core (`QT-PyQt-PySide-Custom-Widgets`)

Licensed under the **GNU Lesser General Public License v3.0 (LGPLv3)**. See
`COPYING.LESSER`.

**What this means for you:**
- ✅ You may use the free core in **proprietary, closed-source applications**,
  including commercial ones, at no cost.
- ✅ You may modify it, but modifications **to the core library itself** must be
  shared under the LGPL (this copyleft applies to the library, not to your app).
- ✅ You must let end users relink your application against a modified version of
  the library (satisfied by normal dynamic import in Python), and include the
  LGPL license text and attribution.

**This is a separate license from Qt's** (see §5). Complying with this license
does not exempt you from complying with Qt's license for the Qt/PySide/PyQt
libraries your application also uses.

---

## 2. The Pro add-on (`custom-widgets-pro`)

`custom-widgets-pro` is **proprietary software**. It is **not** open source and is
**not** covered by the LGPL. It may be used only under a valid entitlement, obtained
through one of the two paths below.

Both paths unlock the **same** Pro widgets. They differ in the **rights granted**
and the **service provided** — not in features.

### 2.1 Commercial License (Gumroad / LemonSqueezy)

For **anyone shipping software for profit** — freelancers, agencies, companies.

**Grants:**
- ✅ The right to use Pro widgets in **commercial, revenue-generating** products.
- ✅ **Priority support** (per your plan's SLA).
- ✅ **Perpetual fallback** — if your subscription lapses, you may continue using
  the **last version released during your active subscription**, indefinitely,
  including in already-shipped and new commercial products covered by your seats.
- ✅ A proper **invoice/receipt** (VAT handled where applicable) you can expense.
- ✅ Updates and new Pro widgets while your subscription is active.

**Seats:** each subscription covers a defined number of **developers** (seats).
Every developer who writes or builds code against `custom-widgets-pro` needs a
seat.

### 2.2 Patreon membership (community tier)

For **personal, non-commercial, and evaluation use** by individuals — hobbyists,
students, and learners.

**Grants:**
- ✅ Access to Pro widgets for **personal, non-commercial, or evaluation**
  projects **while your membership is active**.
- ✅ Community support (Discord).

**Does NOT grant:**
- ❌ The right to use Pro widgets in any **commercial or revenue-generating**
  product (see the definition of Commercial Use in §3).
- ❌ **Perpetual fallback** — access ends when your membership ends. You must stop
  using the Pro add-on for new work once your membership lapses.
- ❌ Priority support or an expensable invoice.

> **In short:** Patreon lets you *learn and build personally while you're a
> member*. A Commercial License gives you the *right to ship for profit, forever,
> with support*.

---

## 3. Definitions

**Commercial Use** — any use of the Pro add-on in connection with a product,
service, or activity that is intended for or directed toward commercial advantage
or monetary compensation. This includes (non-exhaustively): software sold or
licensed to others; internal tools used by a for-profit company; client/contract
work; and revenue-generating apps of **any size**. **There is no revenue threshold
or "small project" exception.**

**Non-Commercial Use** — personal projects, learning, experimentation, academic
coursework, and evaluation, where there is no commercial purpose or compensation.

If you are unsure which applies, assume Commercial Use and obtain a Commercial
License. A **purchasing-power-parity (PPP) discounted individual Commercial
License** is available for eligible regions to keep the legitimate path
affordable.

---

## 4. Royalty-free runtime & prohibitions

### Royalty-free runtime
The Pro add-on requires a valid entitlement **during development and build**.
Applications you build and distribute **run without any license check** and
require **no per-copy or runtime royalty**. You may distribute the compiled Pro
components **inside your own application** as permitted by your entitlement.

### Prohibitions (all entitlements)
You may **not**:
- ❌ Redistribute, resell, sublicense, or publish `custom-widgets-pro` (or its
  wheels, source, or extracted components) as a standalone library or SDK.
- ❌ Extract, decompile, or reuse Pro components from a shipped application for use
  in a separate project.
- ❌ Share, publish, or transfer license keys or Patreon-derived credentials.
- ❌ Circumvent or remove license/entitlement checks.
- ❌ Use the Pro add-on beyond the rights your specific entitlement grants (e.g.
  Commercial Use under a Patreon membership).

Permitted: distributing your **own application** that incorporates the Pro
components in object/compiled form, consistent with your entitlement.

---

## 5. Qt / PySide / PyQt (third-party)

Custom Widgets builds on Qt via `qtpy`, and works with **PySide6** or **PyQt6**.
**You are responsible for complying with the license of the Qt binding you use.**

- **PySide6** is licensed under **LGPLv3** (and commercial). Under LGPL you may
  ship closed-source commercial apps for free if you comply with its terms
  (dynamic linking, allow replacement of the Qt libraries, include notices).
- **PyQt6** (Riverbank) is licensed under **GPLv3** or a **commercial** license.
  Shipping a closed-source app with PyQt6 requires Riverbank's commercial license.

**For commercial, closed-source apps we recommend PySide6**, which is the
supported commercial path and requires no additional Qt payment when you comply
with LGPL.

Neither the free core nor the Pro add-on grants you any rights to Qt, PySide, or
PyQt. "Qt" is a trademark of The Qt Company Ltd. Custom Widgets is an independent,
unofficial project and is not affiliated with or endorsed by The Qt Company or
Riverbank Computing.

---

## 6. Third-party components & assets

The free core and Pro add-on may include or depend on additional third-party
libraries, fonts, and icon sets under their own licenses. A full third-party
license inventory is maintained in `THIRD_PARTY_NOTICES` (to be added). You are
responsible for complying with those licenses in your distributed application.

---

## 7. Warranty & liability

The free core is provided under the LGPL's "as is" terms. The Pro add-on is
provided under its Commercial License Agreement, which contains the applicable
warranty, liability, and indemnity terms. Except as expressly stated in a signed
agreement, the software is provided **"as is" without warranty of any kind**, and
the authors are not liable for any damages arising from its use, to the maximum
extent permitted by law.

---

## 8. Getting a license / questions

- **Buy a Commercial License:** <store links — Gumroad / LemonSqueezy> (TBD)
- **Join on Patreon:** <patreon link> (TBD)
- **Enterprise / custom terms / questions:** <contact email> (TBD)

---

## Appendix — status checklist (remove before publishing)

- [ ] CLA/DCO in place for all contributions
- [ ] Core relicensed GPLv3 → LGPLv3; `COPYING.LESSER` added; root `LICENSE` updated
- [ ] `THIRD_PARTY_NOTICES` inventory generated
- [ ] Commercial License Agreement (full legal text) drafted for the Pro add-on
- [ ] Store links, Patreon link, contact email filled in
- [ ] **Reviewed by qualified legal counsel**
- [ ] Promote this file to `/LICENSING.md`

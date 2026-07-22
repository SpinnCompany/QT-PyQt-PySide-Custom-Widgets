# Commercial product architecture (open-core)

**Status:** Proposed / not started — planning only, implementation later
**Owner:** TBD
**Created:** 2026-07-22
**Related:** modernization-roadmap.md, variant-token-system.md, scss-engine.md

## Summary

Turn Custom Widgets into an open-core commercial product: a **free LGPL core**
that drives adoption, plus a **separate, native-compiled `custom-widgets-pro`
package** gated by a **dual entitlement source** (Gumroad license keys *or*
Patreon membership), sold as an **annual subscription with perpetual fallback**,
delivered via a **store-gated private pip index**. First paid SKU: **DataTable
Pro**. Enforcement is **dev-time only** — shipped apps run royalty-free.

This document records the locked decisions and open questions. No implementation
yet.

## Locked decisions

| Area | Decision |
|---|---|
| **Core license** | Relicense free core GPLv3 → **LGPLv3** (proprietary-app-friendly + legally linkable by closed Pro). Requires CLA. |
| **Package split** | **Separate `custom-widgets-pro`** package, 100% owned, imports the free core, ships compiled wheels. |
| **Code protection** | **Native compile (Cython/Nuitka)** → `.so`/`.pyd`. Real protection; per-OS/arch/Python build matrix. |
| **First SKU** | **DataTable Pro.** |
| **Enforcement** | **Dev-time check, royalty-free runtime.** Perpetual fallback. No runtime check in shipped apps. |
| **Entitlement source** | **Both** — Gumroad/LemonSqueezy license keys (one-off/commercial/B2B) *and* Patreon membership (community tier). One validator accepts either. |
| **Pricing model** | **Subscription + perpetual fallback** — pay for latest + updates + support; keep the last version you had if you cancel. |
| **Delivery** | **Store-gated download + private pip index** — purchase unlocks a key + access to a private index; `pip install custom-widgets-pro` with the key. |

## Package topology

```
custom-widgets           (PUBLIC repo, PyPI, LGPLv3, plain source)   ← free, the funnel
  └── the full widget catalog + tokens/variants + basic DataTable

custom-widgets-pro       (PRIVATE repo, private index, commercial)   ← the product
  ├── depends on: custom-widgets (>= min version)
  ├── DataTable Pro, Charts Pro, Theme Studio, ... (compiled wheels)
  └── custom_widgets_pro.license  (dev-time entitlement validator)

examples/ (public)       Pro examples that import custom-widgets-pro
                         and degrade gracefully (upsell) when unlicensed
```

Rules:
- Free core **must not** depend on Pro. Pro depends on / extends free.
- Pro is new code only — avoids the contributor-relicensing problem entirely.
- A basic DataTable lives in the **free** core (sort/filter/paginate); **Pro**
  adds the hard parts (see SKU scope). Pro's table subclasses/extends the free one.

## Licensing & entitlement design (dev-time)

Goal: a developer must hold a valid entitlement to **develop/build** with Pro;
what they **ship runs forever** without contacting anything.

**One validator, two sources:**
1. **Gumroad/LemonSqueezy key** — verified via the store's license-verify API;
   supports seat/activation limits (LemonSqueezy) and PPP pricing (Gumroad).
2. **Patreon membership** — "Login with Patreon" (OAuth2); read active membership
   + tier via the API; map tier → feature set. Webhooks revoke on cancel.

**Activation flow (design intent):**
- `custom-widgets-pro activate <key>` (or Patreon OAuth) validates once online,
  then writes a **signed local license file** (entitlement + tier + covered
  version range + expiry).
- Subsequent dev use reads the signed file. **Offline grace period** (e.g. N days)
  so devs aren't blocked without network.
- **Perpetual fallback:** the license file encodes the version range it covers;
  after expiry, that version keeps working, but the private index refuses
  newer wheels and support lapses.

**Royalty-free runtime:** the entitlement check is scoped to development. Shipped
apps bundle the compiled Pro and do not validate. Enforcement is therefore
deliberately **soft at runtime** — the real teeth are (a) native compilation
raising extraction cost above the license price, and (b) the **license
agreement**. This is an accepted, standard trade-off (all client-side software).

**Tier → feature mapping** is data-driven (a manifest) so Patreon tiers and store
products both resolve to the same capability set. Ties into the
**component-catalog** hooks from variant-token-system.md.

## First SKU — DataTable Pro (scope)

| Free (in core) | Pro (in custom-widgets-pro) |
|---|---|
| Basic table: sort, filter, paginate, single/multi select | **Virtualization** (100k+ rows, recycled cells) |
| Fixed columns | Column pinning, reorder, resize persistence |
| Read-only cells | **Inline editing** + validation |
| Client-side data | **Server-side / lazy loading** |
| — | **Grouping / pivot / aggregation** |
| — | **CSV / Excel export** |

Build order: basic table in free core first (it's a roadmap Gap #1 item anyway),
then Pro extends it. Depends on the variant/token system for styling.

## Build & release pipeline (later)

- **`cibuildwheel`** to produce the wheel matrix: OS × arch × Python (× Qt binding
  as needed) for the compiled Pro package.
- Publish Pro wheels to a **private index** (self-hosted or a gated service);
  free core to public PyPI.
- Store purchase → key issuance (Gumroad/LS) or membership (Patreon) → private
  index access.

## Prerequisites (must precede any Pro sales)

1. **CLA / DCO** for contributions (enables relicensing).
2. **Relicense core GPLv3 → LGPLv3** (all-contributor consent or rewrite of
   un-clearable files). Aligns with the project's clean-break convention.
3. **`LICENSING.md`** documenting the open-core model + Pro commercial terms
   (royalty-free runtime, perpetual fallback, prohibitions).

## Indicative pricing (from go-to-market analysis; PPP-adjusted)

- Patreon: Pro $15/mo · Studio $50/mo (membership unlocks Pro while subscribed).
- Individual license: ~$99/yr · Team seat: ~$199/yr · Commercial+support:
  $499–1,999/yr. PPP discounts for India/Indonesia/Brazil via the store.

## Patreon vs commercial license — RESOLVED

Differentiate by **rights + service, not features**. Patreon and the paid license
unlock the *same* Pro widgets; the wall between them is the legal grant and the
service level. **No feature-splitting.**

| | Patreon Pro/Studio | Commercial license (Gumroad/LS) |
|---|---|---|
| Audience | Hobbyists, students, personal projects | Freelancers & companies shipping for profit |
| Pro widgets | **All** | **All** |
| License grant | **Non-commercial / personal / evaluation only** | **Commercial use — right to ship for profit** |
| Support | Community (Discord) | **Priority / SLA** |
| Perpetual fallback | ❌ ends with membership | ✅ keep last version forever |
| Invoice / VAT | ❌ | ✅ expensable |

**Why it doesn't cannibalize:** the buyer who'd "just pay $15" is a business, and a
business needs a commercial-use grant, an expensable invoice, and priority support
+ perpetual fallback — none of which Patreon provides. So the $15 tier is a *lower
rung* capturing hobbyists who'd never buy a $199 license anyway (net-new revenue +
funnel), not a substitute for paying customers.

**Leak to plug — the honest small freelancer:** (1) terms state commercial use of
*any* size requires a license (no revenue threshold/exception); (2) offer a
PPP-discounted **individual commercial license** (~$49–99/yr, auto-discounted for
India/Indonesia/Brazil) so the small honest dev has a cheap *legit* path instead
of abusing Patreon.

**Optional (not at launch):** time-delayed access — license holders get new Pro
widgets on release, Patreon members 3–6 months later. Adds separation without
feature-walling. Default off; enable only if data shows Patreon eating license
sales.

**Net rule:** *Patreon = access to learn/build personally while a member. License
= the legal right to ship commercially, forever, with support.* You sell the
right to profit + the service, not the code twice.

## Open questions

- Private index: self-host (devpi/simple index) vs a managed gated service?
- License file signing: key management + how to handle machine transfer/reset.
- LemonSqueezy vs Gumroad as the *primary* key source (LS = tax/invoicing for
  B2B; Gumroad = existing + PPP). Both supported, but which is the default CTA?
- DataTable Pro: virtualization approach (model/view recycling strategy) — decide
  in the SKU implementation spec.
- Anti-piracy ceiling: how much build-matrix cost to spend on native compilation
  vs accepting a softer bar.

## Phased plan (high level — implementation later)

1. **Foundation:** CLA + LGPL relicense + `LICENSING.md`.
2. **Scaffold:** private `custom-widgets-pro` repo + package skeleton + license
   validator (dev-time, dual-source, offline grace).
3. **Basic DataTable in free core** (also closes roadmap Gap #1).
4. **DataTable Pro** as the first compiled SKU.
5. **Delivery:** private index + store integration (Gumroad + Patreon).
6. **Launch** alongside the go-to-market cadence.

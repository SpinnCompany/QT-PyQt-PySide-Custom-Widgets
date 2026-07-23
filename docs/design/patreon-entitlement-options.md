# Patreon entitlement — delivery options

**Status:** Open question — documented, **decide later**. Nothing implemented.
**Created:** 2026-07-23
**Related:** commercial-product.md, datatable-pro-spec.md,
`custom_widgets_pro/_license.py` (Pro repo)

## Context

The commercial model grants Pro entitlement from **two sources** (see
commercial-product.md → "Entitlement source"):

- **Gumroad / LemonSqueezy license keys** — commercial grant. **Fully built and
  live-ready** in `_license.py` (`_verify_gumroad` / `_verify_lemonsqueezy`).
  The store license-verify endpoints are *public* — they need only a non-secret
  `product_id` + the customer's key, **no seller API token**. To go live: bake
  one `_GUMROAD_PRODUCT_ID`.
- **Patreon membership** — non-commercial/community grant. The *verification*
  half (`_verify_patreon` → `/identity`) is built, but the *token-acquisition*
  half is **not**. Getting a patron's OAuth token requires a "Login with
  Patreon" flow, which in turn requires a hosted **broker** (a small service
  holding the `client_secret`, since Patreon has no usable public/PKCE client
  and the secret can't ship inside a distributed wheel).

So Patreon is the only piece with real remaining infrastructure work.

## Option A — Patreon OAuth "Login with Patreon" (the original plan)

Full OAuth: register an OAuth client, run a loopback CLI flow
(`custom-widgets-pro login --patreon`), exchange the code for a token via a
hosted broker, then `activate(patreon_token=...)`.

- **Pros:** membership is checked live against Patreon; churn is automatic (a
  cancelled patron fails at next revalidation); self-serve.
- **Cons:** ~1–2 days of work **plus a hosted broker endpoint you must run and
  maintain forever** (holds `client_secret`); refresh-token handling; more
  moving parts. `_PATREON_CAMPAIGN_ID` must be baked or the check accepts a
  patron of *any* campaign.

## Option B — manual Gumroad keys for patrons (candidate shortcut)

**Idea (2026-07-23):** with **< 100 patrons**, skip Patreon OAuth entirely and
issue **Gumroad license keys** to patrons instead. Patreon becomes a
*distribution channel*, not a separate auth system. Everything flows through the
already-built Gumroad path.

**Mechanism (keys are minted per-purchase, not hand-typed):**

1. Create a dedicated Gumroad product — *"Custom Widgets Pro — Patreon"* —
   price **$0** (or normal price + a 100%-off code posted only in the patron
   feed). Enable *"Generate a unique license key per sale"*.
2. Post the link/code in a **patron-only Patreon post**.
3. Each patron "buys" for $0 → Gumroad **auto-issues a unique key tied to their
   email** and emails it.
4. Patron runs `custom-widgets-pro activate <key>` → existing `_verify_gumroad`
   validates it. No OAuth, no broker, no new code paths.

**Single-use / seat limiting:** flip `increment_uses_count` to `"true"`
(currently `"false"` in `_verify_gumroad`, `_license.py:171`), read back
`body["uses"]`, reject over a small seat cap (~2–3). Gumroad counts activations
server-side per key, so a shared key trips the cap across machines. Keys can
also be disabled individually from the Gumroad dashboard.

**Non-commercial flag:** Gumroad keys currently hard-code `commercial=True`
(`_license.py:182`). Because patrons use a *dedicated* product, map that product
id to `commercial=False` so the rights model stays correct:

```python
# in _verify_gumroad, after the purchase checks
commercial = (product != _PATREON_GUMROAD_PRODUCT_ID)
```

- **Pros:** **zero OAuth, zero broker, zero new infra.** Reuses the built +
  tested Gumroad path. One product + one Patreon post is the entire setup.
  Collapses the dual-source design to a single Gumroad code path (Patreon
  verification can be stubbed/deferred).
- **Cons — churn is manual:** there is no live link to Patreon status. When a
  patron cancels you must **disable their key in the Gumroad dashboard**
  yourself. (Perpetual fallback means they keep the version they had; only
  upgrades re-validate and lock out.) At < 100 patrons this is a ~10-min monthly
  reconcile of the Patreon roster against Gumroad. Also slightly less self-serve
  and not tied to Patreon tier automatically.

## Recommendation (not yet decided)

Lean **Option B** at current scale — it removes the only remaining infra blocker
on the entitlement system and lets Pro ship Gumroad-only, with Patreon as a
distribution channel. Revisit **Option A** if the patron count grows enough that
manual churn management stops being trivial, or if self-serve tier-mapping
becomes important.

**Suggested launch sequencing either way:** ship Gumroad/LS first (needs one
baked product id); treat Patreon delivery as a fast-follow using whichever option
is chosen here.

## If Option B is chosen — code checklist (deferred)

- [ ] Bake `_GUMROAD_PRODUCT_ID` (main commercial product) + a
      `_PATREON_GUMROAD_PRODUCT_ID` constant.
- [ ] `_verify_gumroad`: `increment_uses_count` → `"true"`, enforce seat cap on
      `uses`, map patron product → `commercial=False`.
- [ ] Add the `custom-widgets-pro activate` CLI entry point (no CLI exists yet —
      needs a `__main__.py` + `console_scripts` in `pyproject.toml`).
- [ ] Stub/defer the Patreon OAuth path (`_verify_patreon` verification code can
      stay; no token-acquisition flow needed).
- [ ] Ops runbook: create the $0 patron product, the patron-only post, and the
      monthly churn-reconcile step.

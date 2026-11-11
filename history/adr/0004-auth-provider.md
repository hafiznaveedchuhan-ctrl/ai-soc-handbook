# ADR-0004 — Sign-in provider for the site and the MCP door

- Status: **Proposed — deferred** (owner 2026-11-11: "abhi login skip karo"; revisit before Phase 8)
- Date: 2026-11-11
- Deciders: human:naveed

## Context

Feature 04 turns on the sign-in control the scaffold already ships
(`system/site/components/sign-in.tsx`, `lib/auth/*`). What it needs from a provider is fixed by
that code and by `ksor serve`'s door (`node_modules/@panaversity/ksor/docs/authorization.md`):

1. **OIDC discovery** (`/.well-known/openid-configuration`).
2. A **public client with PKCE** — the site is static files, so it can hold no secret.
3. The token endpoint must accept a **cross-origin browser request** from the site.
4. Later, for the door and the Phase 3 soc-worker: **RS256 JWTs** carrying this record's MCP URL
   in `aud`, and a **machine-to-machine** client.

What sign-in does NOT do (AGENTS.md, config.ts): it protects nothing the static site publishes —
it names the reader. Restricting reading is a hosting decision (Phase 8).

## Options

| Provider | Hosted? | Free to start | Fits 1–4 | ksor recipe | Notes |
|---|---|---|---|---|---|
| **Auth0** | yes | yes (free plan) | yes: SPA app = PKCE no secret; API identifier = `aud`; M2M app for soc-worker | **yes, tested** ("Recipe: Auth0") | Most documented path; three app types to keep apart (the recipe covers it) |
| Keycloak | self-host (Docker) | yes (open source) | yes | **yes** ("Recipe: Keycloak") | We must run and secure a server; `aud` needs a mapper |
| Microsoft Entra ID | yes | yes (free tier) | yes (SPA platform supports PKCE + CORS) | no | Heavier admin; tenant setup |
| Okta (Integrator free) | yes | yes | yes | no | Similar to Auth0, no ksor recipe |
| Google | yes | yes | **no** for (2): a web client needs a client secret at the token endpoint | no | Not usable from a static site alone |

Prices and free-plan limits change — check the provider's current pricing page before creating
the account.

## Recommendation

**Auth0.** It is the only hosted option with a ksor recipe written against a real tenant, it meets
all four needs, and the same tenant later issues the soc-worker's machine-to-machine token for the
door. Keycloak is the fallback if the owner prefers no third-party account.

## Consequences (if Auth0 is chosen)

- Naveed creates the Auth0 account and a **Single Page Application** (callback
  `http://localhost:3000/auth/callback` for dev), and pastes three values into `.env` himself:
  `NEXT_PUBLIC_KSOR_SSO_URL`, `NEXT_PUBLIC_KSOR_OAUTH_CLIENT_ID`, `NEXT_PUBLIC_KSOR_OAUTH_REDIRECT_URI`.
- Claude restyles the control to the SOC console theme, tests sign-in / sign-out, and documents
  plainly that sign-in does not hide any page.
- The API + M2M application (door auth) is created in Phase 3/8, not now.

# Fat Neko — Option B backend (Supabase)

Deploy-ready scaffolding for hosted per-user memory + trade journals. Nothing here is wired into
the live app yet — see `docs/memory-architecture.md` for the why, and
`docs/option-b-client-integration.md` for the in-app adapter to paste at deploy time.

> ⚠️ Reviewed but not yet run end-to-end — needs a real Supabase project + a Telegram bot token.

## Prerequisites
1. A Telegram bot (BotFather) → **bot token** (also needed to publish the Mini App).
2. A Supabase project (free tier is plenty) and the Supabase CLI (`npm i -g supabase`).

## One-time deploy
```bash
supabase login
supabase link --project-ref <your-project-ref>

# database: tables + RLS + storage bucket & policies
supabase db push                 # or paste schema.sql into the SQL editor

# auth edge function (validates Telegram initData, mints a user JWT)
supabase functions deploy tg-auth --no-verify-jwt
supabase secrets set \
  BOT_TOKEN=<from BotFather> \
  SUPABASE_JWT_SECRET=<Project Settings → API → JWT Secret>
```

## Client config (fill in, then wire per the integration doc)
- `SUPABASE_URL`  = `https://<project-ref>.supabase.co`
- `SUPABASE_ANON_KEY` = Project Settings → API → anon public key
- auth endpoint = `${SUPABASE_URL}/functions/v1/tg-auth`

## How it fits together
```
Telegram  →  Mini App (browser)  →  POST /functions/v1/tg-auth { initData }
                                         │  (validates HMAC + auth_date, server-side bot token)
                                         ▼
                                   { token }  ← short-lived Supabase JWT (sub = tg user id)
                                         │
        browser uses token to read/write Storage:  vaults/<tg_id>/memory.md, journal/*.md
        RLS guarantees each user only ever touches their own <tg_id>/ prefix
```

## Files
- `functions/tg-auth/index.ts` — initData validation + JWT minting (Deno edge function)
- `schema.sql` — `memories` table, RLS, `vaults` Storage bucket + object policies

## Security notes
- Bot token + JWT secret live ONLY as edge-function secrets, never in the browser.
- All data access is gated by RLS keyed to the authenticated `sub`; never trust a client-sent id.
- JWTs are short-lived (1h); the client re-auths from `initData` on expiry.

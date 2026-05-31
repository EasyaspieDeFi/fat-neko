# Fat Neko — Multi-User Memory Architecture

**Status:** design doc (no build yet)
**Date:** 2026-05-30
**Context:** Fat Neko is a Telegram Mini App. The AI agent ("the cat") needs per-user
long-term memory + a trade journal. We need this to work for *many* users, not just one.

**Decision:** Option B (hosted per-user vaults on Supabase) is the chosen target. Deploy-ready
scaffolding now exists (reviewed, not yet run end-to-end — needs a live Supabase project + bot):
- `supabase/functions/tg-auth/index.ts` — Telegram `initData` → Supabase JWT edge function
- `supabase/schema.sql` — `memories` table, RLS, `vaults` Storage bucket + policies
- `supabase/README.md` — deploy steps & env vars
- `docs/option-b-client-integration.md` — in-app adapter to wire at deploy time

---

## 1. The core problem

A Telegram Mini App is a **sandboxed browser webview with no backend**. Today the agent is
fully bring-your-own-key (BYOK): each user supplies their own AI provider key, and the browser
calls the provider directly. That works because the user brings the credential.

Memory is different. "Give every user their own private Obsidian vault" means **provisioning
storage on the user's behalf** — that is server-side work. You cannot do it from a pure browser
app, because:

- The browser can't reach the user's local filesystem (no File System Access API in Telegram's
  webview; the Obsidian "Local REST API" plugin is localhost-only and unreachable from a phone).
- Auto-creating a GitHub repo + token per user requires a privileged credential that must never
  live in the browser.

So there's a hard fork: **per-user memory** (easy, already solved) vs **per-user Obsidian-style
markdown vaults for everyone** (needs infrastructure).

---

## 2. What already exists (shipped)

| Capability | Mechanism | Per-user? | Setup | Scales? |
|---|---|---|---|---|
| Long-term memory blob | **Telegram CloudStorage** (`WebApp.CloudStorage`) | ✅ keyed to Telegram user + bot | none | ✅ for a small facts blob |
| Offline fallback | `localStorage` | per-device | none | ✅ |
| Opt-in markdown vault | **GitHub Contents API**, user BYO fine-grained PAT + repo | ✅ (user owns it) | manual (repo + token + Obsidian Git) | ⚠️ power users only |
| Trade journal / note read | GitHub vault tools (`journal_append`, `note_read`) | only when vault connected | manual | ⚠️ power users only |

**Key fact:** CloudStorage is already private and isolated per user, with zero setup. Every user
gets their own memory automatically. CloudStorage limits: ~1024 keys/user, ~4096 chars/value —
fine for a compact facts blob (we cap at 1500 chars), **but too small for a growing journal**.

**Conclusion:** the baseline "each user has their own private memory" requirement is *already met*.
The Obsidian/GitHub vault is an **optional power-user upgrade**, not something to force on everyone.

---

## 3. Requirements for the multi-user target

If we want richer, durable, portable memory for *all* users (not just a CloudStorage blob):

1. **Identity** — securely know which Telegram user is calling, with no passwords.
2. **Isolation** — user A can never read/write user B's data.
3. **Capacity** — store a memory file + an ever-growing journal (well beyond CloudStorage limits).
4. **Markdown-native** — so "open it in Obsidian" is a real, low-friction option.
5. **Cheap at scale** — thousands of users, mostly tiny payloads.
6. **Minimal ops** — ideally no custom servers to babysit.

---

## 4. The keystone: Telegram `initData` auth

Every option below depends on this. Telegram injects a signed `initData` string into the Mini App.
The server validates it to authenticate the user **without any login**:

1. Secret key = `HMAC-SHA256(key="WebAppData", message=BOT_TOKEN)`.
2. Recompute the hash over the sorted `initData` key/values; compare to the provided `hash`.
3. Reject if mismatch or if `auth_date` is stale (e.g. > 24h).
4. On success you trust `user.id` (the stable per-user key) and `first_name`, etc.

The **bot token must stay server-side** — it never touches the browser. This validation is the
only piece of "backend" that's strictly required; it's ~30 lines in a serverless function.

---

## 5. Options

### Option A — CloudStorage default + opt-in BYO vault  *(no backend, ship now)*

- Everyone: memory blob in CloudStorage (already built).
- Power users: connect their own GitHub repo for a real Obsidian vault (already built).
- **Pros:** zero infra, zero cost, ships today, no auth needed.
- **Cons:** journal at scale doesn't fit CloudStorage; non-technical users never get Obsidian.
- **Best for:** launch / MVP. This is the recommended *starting* state.

### Option B — Hosted per-user vaults on Supabase  *(recommended target)*

A backend-as-a-service so we write almost no server code.

- **Auth:** one Supabase **Edge Function** validates Telegram `initData` (§4) and mints a
  short-lived Supabase JWT with `sub = telegram_user_id`.
- **Storage:** Supabase **Storage** bucket, one folder per user:
  `vaults/{tg_id}/memory.md`, `vaults/{tg_id}/journal/2026-05-30.md`, etc.
  Markdown-native → trivially Obsidian-compatible.
- **Isolation:** Row-Level Security / storage policies keyed to `sub` — a user can only touch
  objects under their own `{tg_id}/` prefix. Enforced by the platform, not our code.
- **Browser:** `supabase-js` reads/writes those files directly with the minted JWT. Same
  client-side agent loop, just pointed at Supabase instead of GitHub.
- **Obsidian export (power users):** "Mirror my vault to GitHub" button reuses the *already-built*
  BYO-GitHub path — copy the user's Supabase markdown into their personal repo, which they sync
  with Obsidian Git. So hosted-by-default, portable-on-demand.
- **Pros:** scales, markdown-native, per-user isolation for free, generous free tier, minimal ops.
- **Cons:** requires deploying (a Supabase project + 1 edge function + hosting the static app).
- **Cost:** Supabase free tier = 1GB storage, 500MB DB, 50k MAU auth. Memory/journal payloads are
  KBs; ~10k users ≈ tens of MB. Effectively free until you're large; ~$25/mo Pro after that.

### Option C — App-provisioned GitHub repo per user  *(markdown-native, heaviest)*

- A backend holding a **GitHub App** credential auto-creates a private repo per user and issues a
  scoped installation token.
- **Pros:** every user gets a true git-backed Obsidian vault, no extra export step.
- **Cons:** managing thousands of repos is operationally fragile (rate limits, abuse, cleanup);
  most crypto users don't have/want GitHub; still needs a backend + the §4 auth. Highest risk,
  least upside vs B.
- **Best for:** only if "literally a GitHub repo per user" is a hard product requirement.

---

## 6. Recommendation — phased

1. **Launch (now):** Option A. Per-user CloudStorage memory for everyone + opt-in BYO GitHub vault
   for power users. No new infra. Already built.
2. **At deploy time:** add Option B (Supabase). Move memory + journal to hosted per-user markdown,
   authed via Telegram `initData`. Keep CloudStorage as an offline cache + seed source.
3. **Ongoing power feature:** "Export / mirror to Obsidian (GitHub)" using the existing BYO path.

This sequences cleanly: nothing is wasted, each phase is independently shippable, and we only take
on backend + cost when we actually deploy.

---

## 7. Data model (Option B)

**Storage bucket `vaults` (private), policy: path must start with `auth.jwt() ->> 'sub'`:**

```
vaults/
  {tg_id}/
    memory.md                 # durable facts blob (markdown), source of truth
    watchlist.md              # optional, user/agent maintained
    journal/
      2026-05-30.md           # dated trade-journal notes (append-only)
      2026-05-31.md
```

**Optional DB table for fast lookups / structured facts:**

```sql
create table memories (
  tg_id      bigint primary key,
  facts      text,           -- mirror of memory.md for quick reads
  updated_at timestamptz default now()
);
alter table memories enable row level security;
create policy own_rows on memories
  using (tg_id = (auth.jwt() ->> 'sub')::bigint)
  with check (tg_id = (auth.jwt() ->> 'sub')::bigint);
```

The agent's existing `loadMemory` / `updateMemory` / `journal_append` keep the same shape — only
the read/write backend swaps from GitHub Contents to Supabase Storage/DB.

---

## 8. Security checklist

- Bot token lives **only** in the edge function; never shipped to the browser.
- Validate `initData` HMAC **and** `auth_date` freshness on every token mint.
- All storage/DB access gated by RLS keyed to the authenticated `tg_id` — never trust a client-sent id.
- Minted JWTs short-lived (e.g. 1h); refresh by re-validating `initData`.
- BYO GitHub token (export path) stays client-side, scoped to one private repo (unchanged from today).
- Rate-limit the edge function to blunt abuse.

---

## 9. Migration from today's CloudStorage blob

On first authenticated load under Option B:

1. Read hosted `memory.md`. If it exists → source of truth.
2. If it does **not** exist but a CloudStorage blob does → upload the blob to seed the hosted vault
   (one-time backfill), then continue from hosted.
3. Keep writing a trimmed copy to CloudStorage as an offline cache so the app still works if the
   backend is unreachable.

No user action required; existing users keep their memory.

---

## 10. Open questions

- Do we *require* Obsidian-openability for all users, or is "your data, exportable as markdown"
  enough? (If the latter, Option B fully covers it and Option C is unnecessary.)
- Hosting target for the static Mini App (Cloudflare Pages recommended) — decided at deploy time.
- Journal retention / size policy per user (probably unbounded given tiny payloads).

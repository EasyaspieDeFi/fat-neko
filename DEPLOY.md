# Deploying Fat Neko as a Telegram Mini App

Fat Neko is a single self-contained `index.html` (no build step). Deploying =
**host the file on HTTPS** → **register that URL with @BotFather**.

The data layer (trmnl.pro) and AI (bring-your-own-key) are already production-ready
over HTTPS/CORS, so there is no server to run for the app itself.

---

## 1. Host `index.html` on HTTPS

Telegram requires an `https://` URL. Pick one:

### Option A — GitHub Pages (you already have `ItsTokes/Feed-Fat-Neko`)
1. Push `index.html` to `main` on GitHub.
2. Repo → **Settings → Pages → Source: Deploy from branch → `main` / `(root)`**.
3. Live in ~1 min at `https://itstokes.github.io/Feed-Fat-Neko/index.html`.
   (Repo must be public for free Pages.)

### Option B — Cloudflare Pages (faster CDN, custom domain)
Connect the repo or drag-drop `index.html`; you get a `*.pages.dev` URL.

### Option C — serve from your own infra (trmnl.pro / gitea host)
Serve the static file behind any HTTPS reverse proxy you already run.

> The app is fully absolute-URL'd (fonts, Telegram SDK, trmnl.pro), so it works
> from a sub-path like `/Feed-Fat-Neko/` with no changes.

---

## 2. Create the bot + mini app in @BotFather

1. `/newbot` → choose a name → **save the bot token** (server-side secret; it is
   NOT used by this app and must never be put in `index.html`).
2. `/newapp` → select your bot → set title, description, a 512×512 icon, and the
   **Web App URL** = your hosting URL from step 1 → pick a short name (e.g. `app`).
   You now have a direct link: `https://t.me/<YourBot>/app`.
3. (Optional) `/setmenubutton` → point the bot's menu button at the same URL so the
   chat shows an "Open App" button.

---

## 3. Wire the bot handle (one line of code)

In `index.html`, set the real handle so share/invite deep links resolve:

```js
const APP={bot:"YourBotUsername",app:"app"};   // ~line 205
```

`inviteLink()` builds `https://t.me/<bot>/<app>?startapp=ref_<pid>` from this.

---

## 4. Smoke test

Open `https://t.me/<YourBot>/app` on a phone. The pet, all 3 tabs, the live
Market Pulse, and the agent's trmnl.pro tools should work immediately. Connect a
BYOK AI key in ⚙️ Setup to give the agent its brain.

---

## Before a *public* launch — known gaps

- **Leaderboard is local-only.** "Hall of Chonk" is seeded `localStorage`, NOT a
  shared global board. A real cross-user leaderboard needs a backend (see the
  `supabase/` + `docs/` scaffolding, or add a `/leaderboard` route to trmnl.pro).
- **Shared CoinGlass quota.** Every user's pro-data calls hit trmnl.pro and share
  one CoinGlass hobbyist key. The chrtr backend caches most routes ~60s; add
  rate-limiting/caching if usage grows.
- **Per-user save** already works (Telegram CloudStorage + localStorage mirror).

---

## Repo / hosting reference

- gitea (private): `100.96.165.25:3003/lucy/fat-neko` — `main`
- GitHub: `github.com/ItsTokes/Feed-Fat-Neko`
- Build tag shown in-app: ⚙️ Setup → "build YYYY-MM-DD.x · ↻ reload to latest"

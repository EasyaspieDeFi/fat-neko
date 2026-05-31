# Option B — client integration guide

How the in-app agent swaps its memory backend to Supabase at deploy time. **Do not apply until
deploying** — until then the app stays on Option A (CloudStorage + opt-in GitHub vault).

The design keeps three backends behind one router, in priority order:
1. **Supabase** — when a user JWT was minted (logged-in Telegram user). Source of truth at scale.
2. **GitHub vault** — opt-in power-user override (already built).
3. **CloudStorage / localStorage** — always-on fallback + offline cache (already built).

`memory.md` and `journal/<date>.md` use the *same paths* across Supabase and GitHub, so the agent's
`loadMemory` / `updateMemory` / `journal_append` / `note_read` logic is unchanged — only the
read/write primitives are routed.

---

## 1. Config + auth (add near the AICFG / VAULT block)

```js
// filled in from supabase/README.md at deploy time
const SUPA = { url: "https://<project-ref>.supabase.co", anon: "<anon-public-key>" };
let SBTOK = ""; // short-lived per-user JWT minted by the tg-auth edge function
function supaOn() { return !!(SUPA.url && SUPA.anon && SBTOK); }

async function sbAuth() {                       // call once during init, after tgInit()
  if (!TG || !TG.initData) return false;         // only works inside Telegram
  try {
    const r = await fetch(SUPA.url + "/functions/v1/tg-auth", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ initData: TG.initData }),
    });
    if (!r.ok) return false;
    SBTOK = (await r.json()).token || "";
    return !!SBTOK;
  } catch (e) { return false; }
}

// Storage REST helpers (object path = vaults/<tg_id>/...). RLS enforces the <tg_id> prefix.
function sbHeaders(ct) { const h = { Authorization: "Bearer " + SBTOK, apikey: SUPA.anon }; if (ct) h["content-type"] = ct; return h; }
function sbUrl(path) { return SUPA.url + "/storage/v1/object/vaults/" + path.split("/").map(encodeURIComponent).join("/"); }
async function sbRead(path) {                    // -> text or null
  const r = await fetch(sbUrl(path), { headers: sbHeaders() });
  if (r.status === 404 || r.status === 400) return null;
  if (!r.ok) throw new Error("supa read " + r.status);
  return await r.text();
}
async function sbWrite(path, text) {             // upsert
  const r = await fetch(sbUrl(path), { method: "POST", headers: { ...sbHeaders("text/markdown"), "x-upsert": "true" }, body: text });
  if (!r.ok) throw new Error("supa write " + r.status);
  return true;
}
```

> Note: the per-user folder is `<tg_id>/…`. The client doesn't send the id — it's read from the JWT
> `sub` by RLS. Build paths as `vpath(p)` already does, but rooted at the tg id, e.g.
> `mem path = `${tgId}/memory.md``. Derive `tgId` from `TG.initDataUnsafe.user.id`.

## 2. Router — replace direct `ghRead`/`ghWrite` calls in memory code

```js
function memBackend() { return supaOn() ? "supabase" : (vaultOn() ? "github" : "local"); }

async function memRead(rel) {                    // rel = "memory.md" | "journal/2026-05-30.md"
  if (supaOn())  { const id = TG.initDataUnsafe.user.id; return await sbRead(`${id}/${rel}`); }
  if (vaultOn()) { const m = await ghRead(vpath(rel)); return m ? m.text : null; }
  return null; // local handled by Store in loadMemory
}
async function memWrite(rel, text, msg) {
  if (supaOn())  { const id = TG.initDataUnsafe.user.id; return await sbWrite(`${id}/${rel}`, text); }
  if (vaultOn()) { return await ghWrite(vpath(rel), text, msg); }
  return false; // local handled by Store
}
```

Then in the existing functions, swap the GitHub-specific calls for the router:
- `loadMemory()` → `const text = await memRead("memory.md")` (fall back to `Store.get` if null).
- `updateMemory()` → after computing the blob, `if (memBackend()!=="local") await memWrite("memory.md", ...)`; always keep the `Store.set` cache.
- `journal_append` tool → `await memWrite("journal/"+day+".md", body)`; gate the tool on
  `memBackend()!=="local"` instead of only `vaultOn()`.
- `note_read` tool → `await memRead(path)`.

## 3. Init wiring

```js
// in the init IIFE, after tgInit() and after loading VAULT:
if (SUPA.url && SUPA.anon) await sbAuth();   // mint JWT for the logged-in Telegram user
await loadMemory();                          // now routes Supabase → GitHub → local automatically
```

## 4. Migration (first authed load)

In `loadMemory`, when Supabase is on but `memory.md` doesn't exist yet, seed it from the existing
CloudStorage blob so current users keep their memory:

```js
if (supaOn()) {
  let text = await memRead("memory.md");
  if (text == null) {                                  // no hosted vault yet
    const blob = await Store.get("fatneko_aimem");
    if (blob) { await memWrite("memory.md", "# Fat Neko — what I remember about you\n\n" + blob + "\n"); text = blob; }
  }
  if (text != null) { AIMEM = text.replace(/^#.*\n+/, "").trim(); Store.set("fatneko_aimem", AIMEM); return; }
}
```

## 5. Obsidian export (optional power feature)

Hosted vaults aren't auto-openable in Obsidian. Offer a one-tap **"Mirror to GitHub"** that copies
the user's Supabase markdown into their personal repo via the *already-built* BYO-GitHub path; they
sync that repo with Obsidian Git. So: hosted-by-default for everyone, Obsidian-portable on demand.

## 6. Test plan (at deploy)
1. Open the Mini App inside Telegram → confirm `sbAuth()` mints a token (network 200).
2. Chat a fact → confirm `vaults/<tg_id>/memory.md` appears in Supabase Storage.
3. Ask for a trade idea → confirm `journal/<today>.md` gets an entry.
4. Open as a *second* Telegram user → confirm they cannot see the first user's files (RLS).
5. Kill the network → confirm CloudStorage fallback still serves memory.

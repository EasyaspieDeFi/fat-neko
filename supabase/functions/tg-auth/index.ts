// Fat Neko — Telegram Mini App auth → Supabase JWT  (Option B, §4 of docs/memory-architecture.md)
//
// Validates the signed `initData` Telegram injects into the Mini App, then mints a short-lived
// Supabase-compatible HS256 JWT whose `sub` is the Telegram user id. RLS policies (see schema.sql)
// key every row/object to that `sub`, so the browser can talk to Supabase directly and only ever
// touch its own user's data. The bot token NEVER leaves this function.
//
// Deploy:
//   supabase functions deploy tg-auth --no-verify-jwt
//   supabase secrets set BOT_TOKEN=<from BotFather> SUPABASE_JWT_SECRET=<Project Settings → API → JWT secret>
//
// Client calls: POST { initData } → { token, user:{id,name} }   (401 if initData is invalid/stale)

const BOT_TOKEN = Deno.env.get("BOT_TOKEN")!;
const JWT_SECRET = Deno.env.get("SUPABASE_JWT_SECRET")!;
const MAX_AGE = 86400; // reject initData older than 24h

const enc = new TextEncoder();

function b64url(bytes: Uint8Array): string {
  let s = "";
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function hmac(key: Uint8Array, msg: string): Promise<Uint8Array> {
  const k = await crypto.subtle.importKey("raw", key, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return new Uint8Array(await crypto.subtle.sign("HMAC", k, enc.encode(msg)));
}

// Telegram spec: secret = HMAC_SHA256(key="WebAppData", msg=BOT_TOKEN);
//                hash   = HMAC_SHA256(key=secret, msg=data_check_string)
async function validateInitData(initData: string): Promise<any | null> {
  const params = new URLSearchParams(initData);
  const hash = params.get("hash");
  if (!hash) return null;
  params.delete("hash");
  const dcs = [...params.entries()].map(([k, v]) => `${k}=${v}`).sort().join("\n");
  const secret = await hmac(enc.encode("WebAppData"), BOT_TOKEN);
  const computed = await hmac(secret, dcs);
  const computedHex = [...computed].map((b) => b.toString(16).padStart(2, "0")).join("");
  if (computedHex !== hash) return null;
  const authDate = Number(params.get("auth_date") || 0);
  if (!authDate || Date.now() / 1000 - authDate > MAX_AGE) return null;
  try {
    const user = JSON.parse(params.get("user") || "null");
    return user && user.id ? user : null;
  } catch {
    return null;
  }
}

async function mintJwt(user: any): Promise<string> {
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: "HS256", typ: "JWT" };
  const payload = {
    sub: String(user.id),
    role: "authenticated",
    aud: "authenticated",
    iat: now,
    exp: now + 3600, // 1h; client re-auths from initData when it expires
    tg: { id: user.id, name: user.first_name, username: user.username },
  };
  const data = `${b64url(enc.encode(JSON.stringify(header)))}.${b64url(enc.encode(JSON.stringify(payload)))}`;
  const sig = await hmac(enc.encode(JWT_SECRET), data);
  return `${data}.${b64url(sig)}`;
}

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "content-type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  try {
    const { initData } = await req.json();
    const user = await validateInitData(initData || "");
    if (!user) return json({ error: "invalid or expired initData" }, 401);
    const token = await mintJwt(user);
    return json({ token, user: { id: user.id, name: user.first_name } });
  } catch (e) {
    return json({ error: String(e) }, 400);
  }
});

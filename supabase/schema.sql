-- Fat Neko — Option B per-user memory schema  (docs/memory-architecture.md §7)
-- Apply via Supabase SQL editor, or `supabase db push`.
-- Markdown vaults live in Storage; this table is a fast structured mirror of the facts blob.

-- 1) Structured facts mirror -------------------------------------------------
create table if not exists public.memories (
  tg_id      bigint primary key,
  facts      text not null default '',
  updated_at timestamptz not null default now()
);

alter table public.memories enable row level security;

-- the JWT minted by tg-auth carries the Telegram user id in `sub`
create policy "memories_owner_select" on public.memories
  for select using ((auth.jwt() ->> 'sub')::bigint = tg_id);
create policy "memories_owner_insert" on public.memories
  for insert with check ((auth.jwt() ->> 'sub')::bigint = tg_id);
create policy "memories_owner_update" on public.memories
  for update using ((auth.jwt() ->> 'sub')::bigint = tg_id)
          with check ((auth.jwt() ->> 'sub')::bigint = tg_id);

-- 2) Private Storage bucket for the markdown vaults --------------------------
-- Layout:  vaults/<tg_id>/memory.md , vaults/<tg_id>/journal/2026-05-30.md , ...
insert into storage.buckets (id, name, public)
  values ('vaults', 'vaults', false)
  on conflict (id) do nothing;

-- 3) Storage RLS: a user may only touch objects under their own <tg_id>/ prefix
create policy "vault_owner_select" on storage.objects
  for select using (bucket_id = 'vaults' and (storage.foldername(name))[1] = (auth.jwt() ->> 'sub'));
create policy "vault_owner_insert" on storage.objects
  for insert with check (bucket_id = 'vaults' and (storage.foldername(name))[1] = (auth.jwt() ->> 'sub'));
create policy "vault_owner_update" on storage.objects
  for update using (bucket_id = 'vaults' and (storage.foldername(name))[1] = (auth.jwt() ->> 'sub'));
create policy "vault_owner_delete" on storage.objects
  for delete using (bucket_id = 'vaults' and (storage.foldername(name))[1] = (auth.jwt() ->> 'sub'));

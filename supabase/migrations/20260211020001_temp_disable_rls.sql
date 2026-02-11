-- TEMPORARY: Disable RLS for testing (NOT FOR PRODUCTION)
-- Chỉ dùng để test, sau đó cần enable lại

alter table public.users disable row level security;

-- Hoặc nếu muốn giữ RLS nhưng cho phép insert dễ dàng hơn:
-- drop policy if exists "users_insert_own" on public.users;
-- create policy "users_insert_authenticated"
-- on public.users
-- for insert
-- to authenticated
-- with check (true);

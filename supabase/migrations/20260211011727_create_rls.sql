-- =====================================================
-- ENABLE ROW LEVEL SECURITY
-- =====================================================

alter table public.users enable row level security;
alter table public.game_runs enable row level security;
alter table public.game_scores enable row level security;
alter table public.items enable row level security;
alter table public.user_items enable row level security;

-- =====================================================
-- USERS (profile người chơi)
-- =====================================================

-- Select: chỉ xem profile của mình
create policy "users_select_own"
on public.users
for select
using (auth.uid() = id);

-- Insert: chỉ tạo profile cho chính mình
create policy "users_insert_own"
on public.users
for insert
with check (auth.uid() = id);

-- Update: chỉ sửa profile của mình
create policy "users_update_own"
on public.users
for update
using (auth.uid() = id)
with check (auth.uid() = id);

-- =====================================================
-- GAME_RUNS (lượt chơi)
-- =====================================================

-- Select: chỉ xem run của mình
create policy "runs_select_own"
on public.game_runs
for select
using (auth.uid() = user_id);

-- Insert: chỉ tạo run cho mình
create policy "runs_insert_own"
on public.game_runs
for insert
with check (auth.uid() = user_id);

-- Update: chỉ update run của mình
create policy "runs_update_own"
on public.game_runs
for update
using (auth.uid() = user_id);

-- =====================================================
-- GAME_SCORES (điểm số)
-- =====================================================

-- Select: chỉ xem score của mình (join qua game_runs)
create policy "scores_select_own"
on public.game_scores
for select
using (
  exists (
    select 1
    from public.game_runs gr
    where gr.id = game_scores.run_id
      and gr.user_id = auth.uid()
  )
);

-- Insert: chỉ ghi score cho run của mình
create policy "scores_insert_own"
on public.game_scores
for insert
with check (
  exists (
    select 1
    from public.game_runs gr
    where gr.id = game_scores.run_id
      and gr.user_id = auth.uid()
  )
);

-- =====================================================
-- ITEMS (catalog chung)
-- =====================================================

-- Select: ai cũng xem được
create policy "items_select_all"
on public.items
for select
using (true);

-- =====================================================
-- USER_ITEMS (inventory)
-- =====================================================

-- Select: chỉ xem item của mình
create policy "user_items_select_own"
on public.user_items
for select
using (auth.uid() = user_id);

-- Insert: chỉ thêm item cho mình
create policy "user_items_insert_own"
on public.user_items
for insert
with check (auth.uid() = user_id);

-- Update: chỉ update inventory của mình
create policy "user_items_update_own"
on public.user_items
for update
using (auth.uid() = user_id);

-- =====================================================
-- LEADERBOARD (VIEW công khai)
-- =====================================================

create or replace view public.leaderboard as
select
  u.username,
  max(gs.score) as best_score
from public.game_scores gs
join public.game_runs gr on gs.run_id = gr.id
join public.users u on gr.user_id = u.id
group by u.username;

grant select on public.leaderboard to anon, authenticated;

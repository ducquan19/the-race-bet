-- =========================
-- USERS (profile game)
-- =========================
create table if not exists public.users (
  id uuid primary key
    references auth.users(id) on delete cascade,

  username text unique not null,

  money bigint default 0,
  quantity int default 0,
  num_item int default 0,
  count_item int default 0,

  path text,
  created_at timestamp default now()
);

-- =========================
-- GAME RUNS (1 lần chơi)
-- =========================
create table if not exists public.game_runs (
  id bigserial primary key,

  user_id uuid not null
    references public.users(id) on delete cascade,

  run_index int not null,
  started_at timestamp default now(),
  ended_at timestamp
);

-- =========================
-- GAME SCORES (điểm)
-- =========================
create table if not exists public.game_scores (
  id bigserial primary key,

  run_id bigint not null
    references public.game_runs(id) on delete cascade,

  score int not null,
  created_at timestamp default now()
);

-- =========================
-- ITEMS (optional)
-- =========================
create table if not exists public.items (
  id serial primary key,
  name text not null,
  price int default 0
);

create table if not exists public.user_items (
  id bigserial primary key,

  user_id uuid
    references public.users(id) on delete cascade,

  item_id int
    references public.items(id),

  quantity int default 1
);

-- =========================
-- INDEXES (performance)
-- =========================
create index if not exists idx_users_username
  on public.users(username);

create index if not exists idx_game_runs_user
  on public.game_runs(user_id);

create index if not exists idx_game_scores_run
  on public.game_scores(run_id);

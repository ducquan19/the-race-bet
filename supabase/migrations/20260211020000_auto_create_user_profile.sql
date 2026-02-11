-- =====================================================
-- AUTO CREATE USER PROFILE TRIGGER
-- =====================================================
-- Tự động tạo profile trong bảng users khi có auth user mới

-- Function để tạo user profile
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.users (id, username, money, num_item, count_item, quantity)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
    300,  -- INITIAL_MONEY
    0,
    0,
    0
  );
  return new;
end;
$$ language plpgsql security definer;

-- Trigger khi có user mới trong auth.users
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Grant permissions
grant usage on schema public to anon, authenticated;
grant all on public.users to anon, authenticated;

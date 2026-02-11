-- =====================================================
-- STORAGE BUCKETS FOR LUCKY RACE GAME
-- =====================================================
-- This migration creates storage buckets for:
-- 1. Face ID images (face-images)
-- 2. Game history files (game-history)
-- 3. Game screenshots (game-screenshots)
-- =====================================================

-- =====================================================
-- CREATE STORAGE BUCKETS
-- =====================================================

-- Bucket for Face ID images (private)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'face-images',
    'face-images',
    false,
    5242880, -- 5MB limit per file
    array['image/jpeg', 'image/jpg']
)
on conflict (id) do nothing;

-- Bucket for Game history text files (private)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'game-history',
    'game-history',
    false,
    1048576, -- 1MB limit per file
    array['text/plain']
)
on conflict (id) do nothing;

-- Bucket for Game screenshots (private)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'game-screenshots',
    'game-screenshots',
    false,
    10485760, -- 10MB limit per file
    array['image/png']
)
on conflict (id) do nothing;

-- =====================================================
-- STORAGE POLICIES FOR FACE-IMAGES BUCKET
-- =====================================================
-- Note: Files are stored with path: {username}/{filename}
-- Users can only access files in folders matching their username in users table

-- Policy: Authenticated users can view face images in their username folder
create policy "face_images_select_own"
on storage.objects
for select
using (
    bucket_id = 'face-images'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can upload face images to their username folder
create policy "face_images_insert_own"
on storage.objects
for insert
with check (
    bucket_id = 'face-images'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can update face images in their username folder
create policy "face_images_update_own"
on storage.objects
for update
using (
    bucket_id = 'face-images'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
)
with check (
    bucket_id = 'face-images'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can delete face images in their username folder
create policy "face_images_delete_own"
on storage.objects
for delete
using (
    bucket_id = 'face-images'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- =====================================================
-- STORAGE POLICIES FOR GAME-HISTORY BUCKET
-- =====================================================

-- Policy: Authenticated users can view game history in their username folder
create policy "game_history_select_own"
on storage.objects
for select
using (
    bucket_id = 'game-history'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can upload game history to their username folder
create policy "game_history_insert_own"
on storage.objects
for insert
with check (
    bucket_id = 'game-history'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can update game history in their username folder
create policy "game_history_update_own"
on storage.objects
for update
using (
    bucket_id = 'game-history'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
)
with check (
    bucket_id = 'game-history'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can delete game history in their username folder
create policy "game_history_delete_own"
on storage.objects
for delete
using (
    bucket_id = 'game-history'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- =====================================================
-- STORAGE POLICIES FOR GAME-SCREENSHOTS BUCKET
-- =====================================================

-- Policy: Authenticated users can view screenshots in their username folder
create policy "game_screenshots_select_own"
on storage.objects
for select
using (
    bucket_id = 'game-screenshots'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can upload screenshots to their username folder
create policy "game_screenshots_insert_own"
on storage.objects
for insert
with check (
    bucket_id = 'game-screenshots'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can update screenshots in their username folder
create policy "game_screenshots_update_own"
on storage.objects
for update
using (
    bucket_id = 'game-screenshots'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
)
with check (
    bucket_id = 'game-screenshots'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- Policy: Authenticated users can delete screenshots in their username folder
create policy "game_screenshots_delete_own"
on storage.objects
for delete
using (
    bucket_id = 'game-screenshots'
    and auth.uid() in (
        select id from public.users
        where username = (storage.foldername(name))[1]
    )
);

-- =====================================================
-- VERIFY BUCKETS CREATED
-- =====================================================

-- You can verify buckets with:
-- select * from storage.buckets;

-- You can verify policies with:
-- select * from pg_policies where tablename = 'objects' and schemaname = 'storage';

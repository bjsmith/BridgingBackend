WITH selected_genres AS (
    -- Step 1: Randomly select a limited number of genres
    SELECT genre_id
    FROM genres
    GROUP BY genre_id
    ORDER BY RANDOM()
    LIMIT 5  -- Change this number to limit how many genres you want to randomly select
),
selected_videos AS (
    -- Step 2: For each selected genre, pick one random video with access_count <= 10
    SELECT DISTINCT ON (t.genre_id) t.video_id, t.genre_id, t.access_count
    FROM videos t
    JOIN selected_genres sg ON t.genre_id = sg.genre_id
    WHERE t.access_count <= 10
    ORDER BY t.genre_id, RANDOM()
),
updated_videos AS (
    -- Step 3: Update the access_count for each selected video
    UPDATE videos
    SET access_count = access_count + 1
    WHERE video_id IN (SELECT video_id FROM selected_videos)
    RETURNING video_id, video_creator_username, video_site_id, genre_id -- Return the updated records
)
-- Step 4: Return the selected videos with their updated access_count
SELECT v.video_id, v.video_creator_username, v.video_site_id, ge.title AS genre_title FROM updated_videos v
LEFT JOIN genres ge
on v.genre_id=ge.genre_id
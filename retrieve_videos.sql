WITH selected_genres AS (
    -- Step 1: Randomly select a limited number of genres
    SELECT genre_id
    FROM genres
    ORDER BY RANDOM()
    LIMIT 5  -- Change this number to limit how many genres you want to randomly select
),
all_videos_randomized AS(
    -- Step 2: Randomize the order of all videos with an access count under the threshold
	SELECT * 
	FROM videos v
	WHERE v.access_count <= 10
	ORDER BY v.genre_id, RANDOM()
),
selected_videos AS (
    -- Step 3: For each selected genre, pick one video from the set above
    SELECT DISTINCT ON (v.genre_id) v.video_id, v.genre_id, v.access_count
    FROM all_videos_randomized v
	--must use inner join to select just the videos associated with the selected genres
    INNER JOIN selected_genres sg ON v.genre_id = sg.genre_id 
	ORDER BY v.genre_id
),
updated_videos AS (
    -- Step 4: Update the access_count for each selected video
    UPDATE videos
    SET access_count = access_count + 1
    WHERE video_id IN (SELECT video_id FROM selected_videos)
    RETURNING video_id, video_creator_username, video_site_id, genre_id -- Return the updated records
)
-- Step 4: Return the selected videos with the genre title for each video merged from the genres table
SELECT v.video_id, v.video_creator_username, v.video_site_id, ge.title AS genre_title FROM updated_videos v
LEFT JOIN genres ge
on v.genre_id=ge.genre_id
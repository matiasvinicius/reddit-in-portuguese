SELECT Author.username, 
	   Comment.body, 
	   Comment.created_utc, 
	   Comment.score, 
	   Subreddit.name AS subreddit_name 
FROM Comment
INNER JOIN Subreddit ON Comment.subreddit_id = Subreddit.id
INNER JOIN Author ON Comment.author_id = Author.id
WHERE Comment.created_utc >= '2022-01-01'
ORDER BY Comment.created_utc
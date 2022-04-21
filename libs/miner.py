import sqlite3
from datetime import datetime, timezone
from utils import get_subreddits, create_praw_instace

class Miner():
    def __init__(self):
        self.__reddit = create_praw_instace()
        self.__subreddits = get_subreddits()


    def populate_subreddits(self):
        for name_subreddit in self.__subreddits:
            print(name_subreddit)
            sub = self.__reddit.subreddit(name_subreddit)
            sub_data = (sub.id, 
                        sub.display_name, 
                        sub.description, 
                        sub.subscribers, 
                        datetime.fromtimestamp(sub.created_utc, tz=timezone.utc),
                        sub.over18)

            conn = sqlite3.connect("data/Reddit.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT OR REPLACE INTO Subreddit (id, name, info, subscribers, created_utc, over_18) 
            VALUES (?, ?, ?, ?, ?, ?)""", sub_data)

            conn.commit()
            conn.close()       
        return True


    def __populate_authors(self, author):
        author_id = None
        if author:
            author_id = author.id
            author_data = (author.id, 
                author.name, 
                datetime.fromtimestamp(author.created_utc, tz=timezone.utc),
                author.link_karma,
                author.has_verified_email,
                datetime.now(tz=timezone.utc))

        conn = sqlite3.connect("data/Reddit.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO Author (id, username, created_utc, karma, has_verified_email, last_update) 
        VALUES (?, ?, ?, ?, ?, ?)""", author_data)
        conn.commit()
        conn.close() 
        return author_id

    
    def __populate_comments(self, post):
        for comment in post.comments:
            author_id = self.__populate_authors(post.author)
            comment_data = (comment.id,
                author_id,
                comment.subreddit_id,
                comment.submission.id,
                comment.parent_id,
                comment.body,
                datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                comment.distinguished,
                comment.is_submitter,
                comment.score,
                comment.permalink,
                datetime.now(tz=timezone.utc))
            
            conn = sqlite3.connect("data/Reddit.db")
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO Comment (id, author_id, subreddit_id, submission_id,
            parent_id, body, created_utc, distinguished, is_submitter, score, permalink, last_update) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", comment_data)
            conn.commit()
            conn.close()
            return True

            
    def populate_posts(self):
        for name_subreddit in self.__subreddits:
            print("Mining r/{}".format(name_subreddit))
            sub = self.__reddit.subreddit(name_subreddit)

            for i, post in enumerate(sub.new(limit=1000)):
                try:
                    author_id = self.__populate_authors(post.author)
                    post_data = (post.id, 
                        author_id,
                        post.subreddit.id,
                        post.name,
                        post.title,
                        post.selftext,
                        datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                        post.distinguished,
                        post.is_original_content,
                        post.is_self,
                        post.link_flair_text,
                        post.num_comments,
                        post.over_18,
                        post.permalink,
                        post.score,
                        post.url,
                        post.edited,
                        post.upvote_ratio,
                        datetime.now(tz=timezone.utc))
                    
                    if i % 50 == 0:
                        print(f"Collected {i} posts | Last post date: {post_data[6]}")

                    conn = sqlite3.connect("data/Reddit.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                    INSERT OR REPLACE INTO Submission (id, author_id, subreddit_id, name, title, selftext, created_utc, distinguished, is_original_content,
                    is_self, link_flair_text, num_comments, over_18, permalink, score, url, edited, upvote_ratio, last_update)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", post_data)
                    conn.commit()
                    conn.close() 

                    self.__populate_comments(post)             
                except:
                    pass


if __name__=="__main__":
    miner = Miner()
    #miner.populate_subreddits()
    miner.populate_posts()

import praw
import os

def get_subreddits(path_subs="data/sub_names.txt"):
    with open(path_subs) as f:
        subreddits = f.read().split()
    return subreddits

def create_praw_instace():
    username = os.environ.get("REDDITUSER")
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDITID"),
        client_secret=os.environ.get("REDDITKEY"),
        user_agent=username,
        username=f"research_ptbr by u/{username}"
    )
    return reddit
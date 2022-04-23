import pandas as pd
from sklearn.utils import shuffle
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

def get_top_authors(df):
    n_comments = df.groupby("username")["comment"].count()
    top_authors = n_comments.index[(n_comments>=975) & (n_comments<=1025)]
    df = df[df.username.isin(top_authors)]
    return df

def get_data(csv_path, select_authors=True, remove_duplicates=True):
    df = pd.read_csv(csv_path)
    df = df[["username", "comment", "created_utc"]]
    df = shuffle(df, random_state=42)
    
    if select_authors: df = get_top_authors(df)
    if remove_duplicates: df.drop_duplicates("comment", inplace=True)
    return df
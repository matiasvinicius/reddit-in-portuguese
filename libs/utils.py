from random import random
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

class SparseToArray():
    """
    https://stackoverflow.com/questions/28384680/scikit-learns-pipeline-a-sparse-matrix-was-passed-but-dense-data-is-required
    """

    def __repr__(self):
        return("SparseToArray()")

    def __str__(self):
        return("SparseToArray()")

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None, **fit_params):
        return X.toarray()


def temporal_train_test_split(df, author1, author2):
    data_2authors = df[df.username.isin([author1, author2])]
    data_2authors = data_2authors.sort_values("created_utc")
    train_size = 0.75

    data_author1 = data_2authors[data_2authors.username == author1]
    train_author1 = data_author1[:int(len(data_author1)*train_size)]
    test_author1 = data_author1[int(len(data_author1)*train_size):]

    data_author2 = data_2authors[data_2authors.username == author2]
    train_author2 = data_author2[:int(len(data_author2)*train_size)]
    test_author2 = data_author2[int(len(data_author2)*train_size):]

    X_train = shuffle(pd.concat([train_author1.comment, train_author2.comment]), random_state=42)
    y_train = shuffle(pd.concat([train_author1.username, train_author2.username]), random_state=42)
    X_test = shuffle(pd.concat([test_author1.comment, test_author2.comment]), random_state=42)
    y_test = shuffle(pd.concat([test_author1.username, test_author2.username]), random_state=42)

    return X_train, X_test, y_train, y_test
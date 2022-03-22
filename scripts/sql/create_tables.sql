CREATE TABLE IF NOT EXISTS Author (
    id VARCHAR(15) PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    created_utc DATETIME NOT NULL,
    karma INTEGER,
    has_verified_email BOOLEAN
);

CREATE TABLE IF NOT EXISTS Subreddit (
    id VARCHAR(15) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    info VARCHAR(500),
    subscribers INTEGER NOT NULL,
    created_utc DATETIME NOT NULL,
    over_18 BOOLEAN NOT NULL
);
          
CREATE TABLE IF NOT EXISTS Comment (
    id VARCHAR(15) PRIMARY KEY,
    author_id VARCHAR(15),
    subreddit_id VARCHAR(15) NOT NULL,
    submission_id VARCHAR(15) NOT NULL,
    parent_id VARCHAR(15),
    body TEXT NOT NULL,
    created_utc DATETIME NOT NULL,
    distinguished VARCHAR(10),
    is_submitter BOOLEAN NOT NULL,
    score INTEGER NOT NULL,
    edited BOOLEAN,
    permalink VARCHAR(300),
    FOREIGN KEY (subreddit_id)
        REFERENCES Subreddit (id)
        ON UPDATE RESTRICT
        ON DELETE SET NULL
    FOREIGN KEY (author_id)
        REFERENCES Author (id)
        ON UPDATE RESTRICT
        ON DELETE SET NULL 
    FOREIGN KEY (submission_id)
        REFERENCES Submission (id)
        ON UPDATE RESTRICT
        ON DELETE SET NULL 
    FOREIGN KEY (parent_id)
        REFERENCES Parent_Comment (id_parent)
        ON UPDATE RESTRICT
        ON DELETE SET NULL  
);

CREATE TABLE IF NOT EXISTS Parent_Comment (
    id_comment VARCHAR(15) NOT NULL,
    id_parent VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS Submission (
    id VARCHAR(15) PRIMARY KEY,
    author_id VARCHAR(15) NOT NULL,
    subreddit_id VARCHAR(15) NOT NULL,
    name VARCHAR(300),
    title VARCHAR(300) NOT NULL,
    selftext TEXT NOT NULL,
    created_utc DATETIME NOT NULL,
    distinguished VARCHAR(10),
    is_original_content BOOLEAN NOT NULL,
    is_self BOOLEAN NOT NULL,
    link_flair_text VARCHAR(255),
    num_comments INTEGER NOT NULL,
    over_18 BOOLEAN NOT NULL,
    permalink VARCHAR(255),
    score INTEGER NOT NULL,
    url VARCHAR(300),
    edited BOOLEAN NOT NULL,
    upvote_ratio REAL,
    FOREIGN KEY (subreddit_id)
        REFERENCES Subreddit (id)
        ON UPDATE RESTRICT
        ON DELETE SET NULL
    FOREIGN KEY (author_id)
        REFERENCES Author (id)
        ON UPDATE RESTRICT
        ON DELETE SET NULL 
);
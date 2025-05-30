import praw
import pandas as pd
from datetime import datetime

# Replace these with your credentials
client_id = "6mEjXcZY5QUDqxYEqrDjbg"
client_secret = "zWjcSzYdI8E6zLUOKJ36Udrr3btTKA"
user_agent = "MyScraper by u/BackgroundAlfalfa724"

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Parameters
subreddit_name = "grok"  # Change this to your target subreddit
post_limit = 500               # Number of posts to scrape

# Lists to store data
posts_data = []
comments_data = []

subreddit = reddit.subreddit(subreddit_name)

print(f"Scraping {post_limit} posts from r/{subreddit_name}...")

for submission in subreddit.new(limit=post_limit):
    # Post data
    post_info = {
        "post_id": submission.id,
        "title": submission.title,
        "author": str(submission.author),
        "score": submission.score,
        "created_utc": datetime.fromtimestamp(submission.created_utc),
        "num_comments": submission.num_comments,
        "selftext": submission.selftext,
        "url": submission.url
    }
    posts_data.append(post_info)
    
    # Fetch comments
    submission.comments.replace_more(limit=0)  # Flatten comment tree
    
    for comment in submission.comments.list():
        comment_info = {
            "post_id": submission.id,
            "comment_id": comment.id,
            "author": str(comment.author),
            "score": comment.score,
            "created_utc": datetime.fromtimestamp(comment.created_utc),
            "body": comment.body
        }
        comments_data.append(comment_info)

print("Scraping complete.")

# Save posts and comments to CSV
posts_df = pd.DataFrame(posts_data)
comments_df = pd.DataFrame(comments_data)

posts_df.to_csv("reddit_posts.csv", index=False)
comments_df.to_csv("reddit_comments.csv", index=False)

print("Data saved to 'reddit_posts.csv' and 'reddit_comments.csv'.")

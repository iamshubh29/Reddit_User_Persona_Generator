# reddit_scraper.py
import praw
import time

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            # Test connection - although this doesn't guarantee success later, it's a start
            print("PRAW initialized successfully.")
        except Exception as e:
            print(f"Error initializing PRAW: {e}")
            self.reddit = None # Ensure self.reddit is None if initialization fails

    def scrape_user_profile(self, username, comment_limit=100, submission_limit=50):
        """
        Scrapes comments and posts for a given Reddit username using PRAW.
        Adjust comment_limit and submission_limit to fetch more or less data.
        """
        comments = []
        posts = []

        if not self.reddit:
            print("PRAW not initialized. Cannot scrape.")
            return {"comments": comments, "posts": posts}

        try:
            redditor = self.reddit.redditor(username)
            print(f"Attempting to scrape user: {username}")

            # Fetch comments
            print(f"Fetching {comment_limit} comments...")
            # Use `new` to get most recent, or `top` for highest scoring
            for comment in redditor.comments.new(limit=comment_limit):
                comments.append({"text": comment.body, "url": f"[https://www.reddit.com](https://www.reddit.com){comment.permalink}"})
                # print(f"  Comment: {comment.body[:50]}...") # For debugging
                time.sleep(0.1) # Small delay to be polite to the API

            # Fetch posts (submissions)
            print(f"Fetching {submission_limit} posts...")
            # Use `new` to get most recent, or `top` for highest scoring
            for submission in redditor.submissions.new(limit=submission_limit):
                posts.append({
                    "title": submission.title,
                    "text": submission.selftext if submission.selftext else "", # selftext might be empty for link posts
                    "url": f"[https://www.reddit.com](https://www.reddit.com){submission.permalink}"
                })
                # print(f"  Post: {submission.title[:50]}...") # For debugging
                time.sleep(0.1) # Small delay

            print(f"Scraping complete for {username}. Found {len(comments)} comments and {len(posts)} posts.")

        except praw.exceptions.APIException as e:
            print(f"Reddit API Error for {username}: {e}")
            if "User not found" in str(e) or "User has no submissions" in str(e) or "User has no comments" in str(e):
                print(f"User '{username}' either does not exist or has no public content.")
            elif "Too many requests" in str(e):
                print("Rate limit hit. Please wait and try again later or reduce limits.")
        except Exception as e:
            print(f"An unexpected error occurred during Reddit scraping for {username}: {e}")

        return {"comments": comments, "posts": posts}
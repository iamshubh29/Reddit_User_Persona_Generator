# main.py
import argparse
import os
from dotenv import load_dotenv

from reddit_scraper import RedditScraper
from persona_builder import PersonaBuilder

def main():
    load_dotenv() # Load environment variables from .env

    parser = argparse.ArgumentParser(description="Generate a user persona from a Reddit profile.")
    parser.add_argument("reddit_url", type=str, help="The URL of the Reddit user profile (e.g., [https://www.reddit.com/user/kojied/](https://www.reddit.com/user/kojied/))")
    args = parser.parse_args()

    # Extract username from the URL
    username = args.reddit_url.strip('/').split('/')[-1]
    output_filename = os.path.join("output", f"{username}_persona.txt")

    print(f"Starting persona generation for user: {username}")

    # Initialize RedditScraper with PRAW credentials from .env
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT")

    if not all([reddit_client_id, reddit_client_secret, reddit_user_agent]):
        print("Error: Reddit API credentials (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT) are not set correctly in the .env file.")
        print("Please ensure you have filled them from your Reddit app settings.")
        return

    scraper = RedditScraper(reddit_client_id, reddit_client_secret, reddit_user_agent)

    scraped_data = scraper.scrape_user_profile(username)

    if not scraped_data["comments"] and not scraped_data["posts"]:
        print(f"No significant public comments or posts found for user {username}. Cannot build a detailed persona.")
        # Create an empty or basic persona file to indicate completion, if desired
        os.makedirs("output", exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"No significant public comments or posts found for Reddit user: {username}.\n"
                    f"Persona could not be built based on public activity.")
        print(f"Empty persona file saved to {output_filename}")
        return

    # Initialize PersonaBuilder with Gemini API Key from .env
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key or google_api_key == "YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY_HERE":
        print("Error: Google Gemini API Key (GOOGLE_API_KEY) is not set or is still the placeholder in the .env file.")
        print("Please obtain your key from Google AI Studio and update the .env file.")
        return

    persona_builder = PersonaBuilder(google_api_key)
    user_persona_with_citations = persona_builder.build_persona(scraped_data)

    os.makedirs("output", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(user_persona_with_citations)
    print(f"User persona saved to {output_filename}")

if __name__ == "__main__":
    main()
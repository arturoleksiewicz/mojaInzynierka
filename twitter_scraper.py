from scrapfly import ScrapflyClient, ScrapeConfig
from typing import Dict

scrapfly = ScrapflyClient(key="scp-live-569ac008a42f41b4b3d0bb8596ccec3d")

from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup
import time



def scrape_recent_tweets(username: str, tweet_count: int = 10) -> dict:
    """
    Scrape the most recent tweets from a Twitter profile.
    :param username: Twitter username without '@'
    :param tweet_count: Number of recent tweets to scrape
    :return: A dictionary containing the scraped tweets and profile information.
    """
    profile_url = f"https://x.com/{username}"
    tweets = []
    max_tweets = tweet_count

    # Define the scraping configuration
    scrape_config = ScrapeConfig(
        url=profile_url,
        render_js=True,  # Enable JavaScript rendering
        wait_for_selector="[data-testid='primaryColumn']",  # Wait for the profile's tweet section to load
        country="US",  # Optional: Use a proxy from a specific country
        screenshots={"all": "fullpage"}  # Optional: Capture screenshots for debugging
    )

    # Scrape the page and get the first batch of tweets
    result = scrapfly.scrape(scrape_config)
    page_content = result.content

    # Parsing the profile and tweet details using BeautifulSoup
    soup = BeautifulSoup(page_content, "html.parser")

    # Scraping profile information
    profile_data = {}
    name_tag = soup.select_one("[data-testid='UserName']")
    profile_data['name'] = name_tag.text if name_tag else "N/A"

    bio_tag = soup.select_one("[data-testid='UserDescription']")
    profile_data['bio'] = bio_tag.text if bio_tag else "No bio available"

    followers_tag = soup.select_one("[href$='/followers']")
    following_tag = soup.select_one("[href$='/following']")
    profile_data['followers_count'] = followers_tag.text if followers_tag else "N/A"
    profile_data['following_count'] = following_tag.text if following_tag else "N/A"

    # Function to extract tweets from page content
    def extract_tweets(soup: BeautifulSoup):
        tweet_tags = soup.select("[data-testid='tweet']")
        for tweet_tag in tweet_tags:
            tweet_content = tweet_tag.select_one("[lang]")
            tweet_text = tweet_content.text if tweet_content else "N/A"

            # Extract metadata like tweet time, likes, retweets, etc.
            tweet_time = tweet_tag.select_one("time")['datetime'] if tweet_tag.select_one("time") else "N/A"

            # Add the tweet to the list
            tweets.append({
                'text': tweet_text,
                'time': tweet_time
            })
            if len(tweets) >= max_tweets:
                break

    # Initial tweet extraction
    extract_tweets(soup)

    # Scroll and load more tweets until we reach 100 tweets
    while len(tweets) < max_tweets:
        time.sleep(1)  # Add delay to simulate user scrolling
        scrape_config.scroll_page = True  # Enable automatic scrolling to load more tweets
        result = scrapfly.scrape(scrape_config)
        soup = BeautifulSoup(result.content, "html.parser")
        extract_tweets(soup)
        print(f"Scraped {len(tweets)} tweets...")

    profile_data['tweets'] = tweets[:max_tweets]
    return profile_data


if __name__ == "__main__":
    username = input("Enter the Twitter profile username: ")
    profile_info = scrape_recent_tweets(username, tweet_count=100)
    print(f"Profile Info: {profile_info['name']}")
    print(f"Followers: {profile_info['followers_count']}")
    print(f"Following: {profile_info['following_count']}")
    print("\nRecent Tweets:")
    for i, tweet in enumerate(profile_info['tweets'], 1):
        print(f"{i}. {tweet['time']}: {tweet['text']}\n")

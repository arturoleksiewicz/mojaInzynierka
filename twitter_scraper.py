from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup
import time
import os

scrapfly = ScrapflyClient(key=os.getenv("scrapfly"))

def scrape_recent_tweets(username: str, tweet_count: int = 1, max_attempts: int = 3) -> dict:
    profile_url = f"https://x.com/{username.replace(' ', '-').lower()}"
    tweets = []
    max_tweets = tweet_count

    scrape_config = ScrapeConfig(
        url=profile_url,
        render_js=True,
        wait_for_selector="[data-testid='primaryColumn']",
        country="US",
        screenshots={"all": "fullpage"}
    )
    attempt = 0

    def extract_tweets(soup: BeautifulSoup):
        tweet_tags = soup.select("[data-testid='tweet']")
        for tweet_tag in tweet_tags:
            tweet_content = tweet_tag.select_one("[lang]")
            tweet_text = tweet_content.text if tweet_content else "N/A"


            tweet_time = tweet_tag.select_one("time")['datetime'] if tweet_tag.select_one("time") else "N/A"
            tweets.append({
                'text': tweet_text,
                'time': tweet_time
            })
            if len(tweets) >= max_tweets:
                break

    profile_data = {}

    while len(tweets) < max_tweets and attempt < max_attempts:
        try:
            print(f"Attempt {attempt + 1} to scrape tweets...")
            result = scrapfly.scrape(scrape_config)
            page_content = result.content
            soup = BeautifulSoup(page_content, "html.parser")

            if attempt == 0:
                name_tag = soup.select_one("[data-testid='UserName']")
                profile_data['name'] = name_tag.text if name_tag else "N/A"

                bio_tag = soup.select_one("[data-testid='UserDescription']")
                profile_data['bio'] = bio_tag.text if bio_tag else "No bio available"

                followers_tag = soup.select_one("[href$='/followers']")
                following_tag = soup.select_one("[href$='/following']")
                profile_data['followers_count'] = followers_tag.text if followers_tag else "N/A"
                profile_data['following_count'] = following_tag.text if following_tag else "N/A"

            extract_tweets(soup)
            if len(tweets) >= max_tweets:
                break

        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")

        attempt += 1
        time.sleep(1)

    if len(tweets) == 0:
        return {"error": f"Failed to scrape tweets after {max_attempts} attempts."}

    profile_data['tweets'] = tweets[:max_tweets]
    return profile_data


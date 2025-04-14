from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import re

class NewsAPIFetcher:
    def __init__(self, api_key, analyze_sentiment=False, summarize_articles=False):
        self.api_key = api_key
        self.analyze_sentiment = analyze_sentiment
        self.summarize_articles = summarize_articles
        self.summarizer = pipeline("summarization") if summarize_articles else None
        self.sentiment_analyzer = pipeline("sentiment-analysis") if analyze_sentiment else None

    def fetch_news(self, search_phrase, max_results=10):
        url = f"https://newsapi.org/v2/everything?q={search_phrase}&apiKey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            news_articles = response.json()
        else:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )

        # Filter and collect valid articles
        articles = []
        count = 0
        for article in news_articles["articles"]:
            if count >= max_results:
                break

            url = article.get("url", "")
            title = article.get("title", "")

            try:
                content = self.extract_article_content(url)
                # Check if content is valid
                if not content.strip() or "removed" in content.lower() or "coming soon" in content.lower():
                    continue

                # Perform sentiment analysis if enabled
                sentiment = self.perform_sentiment_analysis(content) if self.analyze_sentiment else "Not analyzed"

                # Summarize article if enabled
                summary = self.summarize_article(content) if self.summarize_articles else "Not summarized"

                articles.append({
                    "url": url,
                    "title": title,
                    "content": content,
                    "summary": summary,
                    "sentiment": sentiment
                })
                count += 1  # Increment count only for valid articles
            except Exception as e:
                # Log or print exception if necessary
                print(f"Error processing article: {title}, URL: {url}, Error: {e}")

        return articles

    def extract_article_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article_content = ""
        for paragraph in soup.find_all("p"):
            article_content += paragraph.text + "\n"
        return self.preprocess_content(article_content)

    def preprocess_content(self, content):
        # Remove URLs and certain irrelevant keywords (adjust according to your needs)
        content = re.sub(r'http\S+', '', content)  # Remove URLs
        content = re.sub(r'(iPhone|IFA 2024)', '', content)  # Example: Remove unrelated product names
        return content

    def perform_sentiment_analysis(self, text):
        if self.sentiment_analyzer:
            sentiment_results = self.sentiment_analyzer(text[:512])  # Use only the first 512 tokens for analysis
            if sentiment_results:
                return sentiment_results[0]["label"]
        return "Unknown"

    def summarize_article(self, text):
        if self.summarizer:
            summary = self.summarizer(text, max_length=100, min_length=30, do_sample=False)
            return summary[0]['summary_text'] if summary else "Summary not available"
        return "Summary not available"


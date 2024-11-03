from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re

from transformers import pipeline


# Optionally, use transformers for more advanced summarization
# from transformers import pipeline

class NewsAPIFetcher:
    def __init__(self, api_key, analyze_sentiment=False, summarize_articles=False, use_advanced_summarizer=False):
        self.api_key = api_key
        self.analyze_sentiment = analyze_sentiment  # Analyze sentiment flag
        self.summarize_articles = summarize_articles  # Summarize articles flag
        self.use_advanced_summarizer = use_advanced_summarizer  # Use transformers summarizer if True

        # Initialize the transformers summarizer if advanced summarization is enabled
        if self.use_advanced_summarizer:
            self.summarizer = pipeline("summarization")

    def fetch_news(self, search_phrase, max_results=10):
        url = f"https://newsapi.org/v2/everything?q={search_phrase}&apiKey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            news_articles = response.json()
            article_urls = [article["url"] for article in news_articles["articles"][:max_results]]
            article_titles = [article["title"] for article in news_articles["articles"][:max_results]]
        else:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )

        articles = []
        for url, title in zip(article_urls, article_titles):
            content = self.extract_article_content(url)
            sentiment = self.perform_sentiment_analysis(content) if self.analyze_sentiment else "Not analyzed"
            summary = self.summarize_article(content) if self.summarize_articles else content  # Summarize if flag is set
            articles.append({
                "url": url,
                "title": title,
                "content": content,
                "summary": summary,  # Add summary to the article data
                "sentiment": sentiment
            })

        return articles

    def extract_article_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article_content = ""
        for paragraph in soup.find_all("p"):
            article_content += paragraph.text + "\n"
        return self.preprocess_content(article_content)  # Apply preprocessing

    def preprocess_content(self, content):
        # Remove URLs and certain irrelevant keywords (adjust according to your needs)
        content = re.sub(r'http\S+', '', content)  # Remove URLs
        content = re.sub(r'(iPhone|IFA 2024)', '', content)  # Example: Remove unrelated product names
        # Add more filtering if necessary
        return content

    def perform_sentiment_analysis(self, text):
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity
        if sentiment_score > 0:
            return "Positive"
        elif sentiment_score < 0:
            return "Negative"
        else:
            return "Neutral"

    def summarize_article(self, text):
        if self.use_advanced_summarizer:
            return self.advanced_summarization(text)
        else:
            return self.simple_summarization(text)

    def simple_summarization(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 2)  # Limit to 2 sentences
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        return summary

    def advanced_summarization(self, text):
        # Using the transformers-based summarizer for better-quality summaries
        summary = self.summarizer(text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']

import requests
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from langdetect import detect
from transformers import pipeline
import os
nltk.download('punkt')
nltk.download('stopwords')


class NewsSentimentAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        try:
            self.summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
        except Exception as e:
            print(f"Failed to load summarizer model: {e}")
            self.summarizer = None

    def fetch_news_articles(self, search_phrase, max_results=10):
        url = f"https://newsapi.org/v2/everything?q={search_phrase}&apiKey={self.api_key}&pageSize={max_results}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [(article['title'], article['description'], article['content']) for article in articles]
        else:
            raise Exception(f"Failed to fetch news: {response.status_code} - {response.text}")

    def preprocess_text(self, text, language='en'):
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalpha()]

        stop_words = set(stopwords.words(language))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        return ' '.join(filtered_tokens)

    def analyze_sentiment(self, text):
        if not text:
            return 0.0, 0.0

        try:
            language = detect(text)
        except Exception as e:
            print(f"Language detection failed: {e}")
            language = 'en'

        processed_text = self.preprocess_text(text, language)
        sentiment = TextBlob(processed_text).sentiment

        return sentiment.polarity, sentiment.subjectivity

    def summarize_article(self, text):
        if self.summarizer:
            try:
                summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
                return summary[0]['summary_text']
            except Exception as e:
                print(f"Summarization failed: {e}")
                return "Summarization failed"
        else:
            return "Summarizer not available"

    def analyze_news_sentiments(self, search_phrase):
        articles = self.fetch_news_articles(search_phrase)
        results = []
        for title, description, content in articles:
            if content:
                summary = self.summarize_article(content)
                polarity, subjectivity = self.analyze_sentiment(content)
                results.append((title, summary, polarity, subjectivity))
            else:
                results.append((title, "No content available", 0.0, 0.0))  # Neutral sentiment if no content

        return results


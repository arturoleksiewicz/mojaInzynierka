from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NewsSentimentAnalyzer:
    def __init__(self):
        # Initialize the sentiment intensity analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, articles):
        """
        Analyze the sentiment of each article in the list of articles.
        :param articles: List of dictionaries containing article content and URL.
        :return: List of articles with sentiment scores (positive, negative, neutral).
        """
        analyzed_articles = []
        for article in articles:
            # Get the article content and analyze its sentiment
            content = article.get('content', '')
            if content:
                sentiment = self.analyzer.polarity_scores(content)
                article['sentiment'] = self._get_sentiment_label(sentiment['compound'])
            else:
                article['sentiment'] = 'No content available'

            # Append the article with sentiment to the new list
            analyzed_articles.append(article)

        return analyzed_articles

    def _get_sentiment_label(self, score):
        """
        Convert the compound score to a sentiment label.
        :param score: Compound score from VADER sentiment analysis.
        :return: Sentiment label (positive, neutral, negative).
        """
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

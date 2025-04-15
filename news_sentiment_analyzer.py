from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NewsSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, articles):
        analyzed_articles = []
        for article in articles:
            content = article.get('content', '')
            if content:
                sentiment = self.analyzer.polarity_scores(content)
                article['sentiment'] = self._get_sentiment_label(sentiment['compound'])
            else:
                article['sentiment'] = 'No content available'

            analyzed_articles.append(article)

        return analyzed_articles

    def _get_sentiment_label(self, score):

        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

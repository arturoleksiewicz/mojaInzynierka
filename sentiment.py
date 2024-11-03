import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from googletrans import Translator, LANGUAGES
import os
import sys
import contextlib

@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

def preprocess_text(text, language):
    try:
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalpha()]

        if language in stopwords.fileids():
            stop_words = set(stopwords.words(language))
        else:
            stop_words = set(stopwords.words('english'))

        tokens = [word for word in tokens if word not in stop_words]
        processed_text = ' '.join(tokens)

        return processed_text
    except Exception as e:
        print(f"Error in preprocessing text: {e}")
        return text

def analyze_sentiment(text):
    try:
        language = detect(text)
        if language not in LANGUAGES:
            language = 'en'
    except LangDetectException:
        language = 'en'
    processed_text = preprocess_text(text, language)

    if language != 'en':
        try:
            translator = Translator()
            translated = translator.translate(processed_text, dest='en')
            processed_text = translated.text
        except Exception as e:
            print(f"Translation error: {e}")
            return 'Neutralny'

    analysis = TextBlob(processed_text)
    sentiment_polarity = analysis.sentiment.polarity

    if sentiment_polarity > 0.2:
        return 'Pozytywny'
    elif sentiment_polarity < -0.2:
        return 'Negatywny'
    else:
        return 'Neutralny'

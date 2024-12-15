
import random
import time
import requests
import warnings
from google_search import GoogleSearchFetcher
from googleTrends import GoogleTrendsFetcher
from ibisworld import IbisWorldFetcher
from linkedin_fetcher import LinkedinFetcher
from statista import StatistaFetcher
from trustpilot import TrustpilotFetcher
from yahooFinance import YahooFinanceFetcher
from wikipedia_fetcher import WikipediaFetcher
from newsapi_fetcher import NewsAPIFetcher
from twitter_scraper import scrape_recent_tweets
from shodan_fetcher import ShodanFetcher
from hackertarget_fetcher import HackerTargetFetcher
from vt_fetcher import VirusTotalFetcher


warnings.filterwarnings('ignore', category=UserWarning, module='bs4')
warnings.filterwarnings('ignore', category=FutureWarning, module='transformers')

class CompanyInfoFetcher:
    def __init__(self, company_name, selected_sources, analyze_sentiment=False, summarize_articles=False):
        self.company_name = company_name
        self.selected_sources = selected_sources
        self.analyze_sentiment = analyze_sentiment
        self.summarize_articles = summarize_articles

        if "IBISWorld" in selected_sources:
            self.ibisworld_fetcher = IbisWorldFetcher()

        if "LinkedIn" in selected_sources:
            self.linkedin_fetcher = LinkedinFetcher(username="artur.oleksiewicz.work@gmail.com", password="Sto1noga$")

        if "Statista" in selected_sources:
            self.statista_fetcher = StatistaFetcher()

        if "Trustpilot" in selected_sources:
            self.trustpilot_fetcher = TrustpilotFetcher()

        if "YahooFinance" in selected_sources:
            self.yahoofinance_fetcher = YahooFinanceFetcher(file_path="nasdaqList.csv")

        if "GoogleTrends" in selected_sources:
            self.google_trends_fetcher = GoogleTrendsFetcher()

        if "GoogleSearch" in selected_sources:
            self.google_search_fetcher = GoogleSearchFetcher(
                api_key="e4017084ad01edc1cad1f43656c4551b6723ef1e76f6cb6e208cd7d0a2291587")

        if "News" in selected_sources:
            self.news_api_fetcher = NewsAPIFetcher(api_key="6225ddb8a62e48b499e22f8614264114",
                                                   analyze_sentiment=self.analyze_sentiment,
                                                   summarize_articles=self.summarize_articles)

        if "Wikipedia" in selected_sources:
            self.wikipedia_fetcher = WikipediaFetcher()

        if "X.com" in selected_sources:
            self.twitter_username = company_name  # Assuming the company_name is the Twitter username

        if "Shodan" in selected_sources:
            self.shodan_fetcher = ShodanFetcher(api_key="JGoNDkBK729GYLe0ofEVYtQvHuE6FBmV")

        if "HackerTarget" in selected_sources:
            self.hackertarget_fetcher = HackerTargetFetcher()


        if "VirusTotal" in selected_sources:
            self.virustotal_fetcher = VirusTotalFetcher(
                api_key="964657e55676c6ab97a21a9e8cda62fad825c3c2b8d30306822653b7a661fa90")

    def fetch_all_info(self):
        company_info = {}

        if "IBISWorld" in self.selected_sources:
            company_info["IBISWorld Data"] = self._retry_request(self.ibisworld_fetcher.search_ibisworld,
                                                                 self.company_name)

        if "LinkedIn" in self.selected_sources:
            company_info["LinkedIn Data"] = self.linkedin_fetcher.get_linkedin_data(self.company_name)

        if "Statista" in self.selected_sources:
            company_info["Statista Data"] = self._retry_request(self.statista_fetcher.search_statista,
                                                                self.company_name)

        if "Trustpilot" in self.selected_sources:
            try:
                company_info["Trustpilot Data"] = self.trustpilot_fetcher.search_trustpilot(self.company_name)
            except requests.ConnectionError:
                company_info["Trustpilot Data"] = "Trustpilot data could not be retrieved due to a connection error."

        if "YahooFinance" in self.selected_sources:
            matched_company_name, ticker_symbol, yahoo_finance_data = self.yahoofinance_fetcher.fetch_stock_data(
                self.company_name)
            company_info["Yahoo Finance Data"] = {
                "Matched Company Name": matched_company_name,
                "Ticker Symbol": ticker_symbol,
                "Stock Data": yahoo_finance_data  # Teraz zawiera daty
            }

        if "GoogleTrends" in self.selected_sources:
            company_info["Google Trends Image"] = self._retry_request(self.google_trends_fetcher.fetch_google_trends,
                                                                      self.company_name)

        if "GoogleSearch" in self.selected_sources:
            company_info["Google Search Results"] = self._retry_request(self.google_search_fetcher.google_search,
                                                                        self.company_name + " company news")

        if "News" in self.selected_sources:
            company_info["News Data"] = self._retry_request(self.news_api_fetcher.fetch_news, self.company_name)

        if "Wikipedia" in self.selected_sources:
            company_info["Wikipedia Data"] = self.wikipedia_fetcher.get_company_info(self.company_name)

        if "X.com" in self.selected_sources:
            company_info["X.com Tweets"] = scrape_recent_tweets(self.twitter_username)

        if "Shodan" in self.selected_sources:
            company_info["Shodan Data"] = self.shodan_fetcher.fetch_shodan_info(self.company_name)

        if "HackerTarget" in self.selected_sources:
            company_info["HackerTarget Data"] = self.hackertarget_fetcher.run_all_hackertarget_functions(
                self.company_name
            )


        if "VirusTotal" in self.selected_sources:
            company_info["VirusTotal Data"] = self.virustotal_fetcher.check_website_in_virustotal(self.company_name)

        return company_info

    def _retry_request(self, func, *args, retries=5):
        for attempt in range(retries):
            try:
                return func(*args)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"Too many requests error on attempt {attempt + 1}. Retrying after delay...")
                    time.sleep(2 ** attempt + random.random())  # Exponential backoff with random jitter
                else:
                    print(f"An unexpected HTTP error occurred: {e}")
                    break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
        return f"Failed to retrieve {func.__name__} data after several attempts."

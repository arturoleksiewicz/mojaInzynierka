import time
import pandas as pd
from fuzzywuzzy import process
from polygon import RESTClient, exceptions


class PolygonFetcher:
    def __init__(self, api_key, file_path):
        self.client = RESTClient(api_key)
        self.company_data = pd.read_csv(file_path)
        self.company_dict = pd.Series(self.company_data.Symbol.values, index=self.company_data.Name).to_dict()
        self.company_names = list(self.company_dict.keys())

    def _get_ticker(self, company_name):
        best_match = process.extractOne(company_name, self.company_names)
        if best_match:
            return self.company_dict[best_match[0]]
        return None

    def _retry_request(self, func, *args, retries=5):
        for attempt in range(retries):
            try:
                return func(*args)
            except exceptions.BadResponse as e:
                if e.status == 429:
                    print(f"Too many requests error on attempt {attempt + 1}. Retrying after delay...")
                    time.sleep(2 ** attempt)  # Exponential backoff

                else:
                    print(f"An unexpected error occurred: {e}")
                    break
        print("Failed to retrieve data after several attempts.")
        return []

    def fetch_aggregates(self, company_name):
        ticker = self._get_ticker(company_name)
        if not ticker:
            return f"Company name '{company_name}' not found in the list."

        try:
            aggs = list(self.client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2023-06-12",
                                              to="2024-06-13", limit=500))
            return aggs
        except exceptions.BadResponse as e:
            return f"Error fetching aggregates: {e}"

    def fetch_last_trade(self, company_name):
        ticker = self._get_ticker(company_name)
        if not ticker:
            return f"Company name '{company_name}' not found in the list."

        return self._retry_request(self.client.get_last_trade, ticker)

    def fetch_last_quote(self, company_name):
        ticker = self._get_ticker(company_name)
        if not ticker:
            return f"Company name '{company_name}' not found in the list."

        return self._retry_request(self.client.get_last_quote, ticker)

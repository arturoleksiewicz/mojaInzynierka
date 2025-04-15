import pandas as pd
import yfinance as yf
from fuzzywuzzy import process


class YahooFinanceFetcher:
    def __init__(self, file_path):
        self.company_data = pd.read_csv(file_path)
        self.company_dict = pd.Series(self.company_data.Symbol.values, index=self.company_data.Name).to_dict()
        self.company_names = list(self.company_dict.keys())

    def fetch_stock_data(self, company_name):
        best_match = process.extractOne(company_name, self.company_names)

        if best_match:
            matched_company_name, score = best_match
            ticker_symbol = self.company_dict[matched_company_name]
            print(f"Best match: {matched_company_name} with score {score}")
            print(f"Ticker symbol: {ticker_symbol}")

            try:
                stock_info = yf.Ticker(ticker_symbol)
                history = stock_info.history(period="1mo")

                if history.empty:
                    print(f"No stock data available for ticker symbol: {ticker_symbol}")
                    return matched_company_name, ticker_symbol, []

                print(f"Stock data retrieved for {ticker_symbol}:")
                print(history.head())
                stock_data = [
                    {
                        "Date": date.strftime('%Y-%m-%d'),
                        "Open": row["Open"],
                        "High": row["High"],
                        "Low": row["Low"],
                        "Close": row["Close"],
                        "Volume": row["Volume"]
                    }
                    for date, row in history.iterrows()
                ]

                return matched_company_name, ticker_symbol, stock_data

            except Exception as e:
                print(f"Error fetching stock data for {ticker_symbol}: {e}")
                return matched_company_name, ticker_symbol, []

        else:
            print(f"No match found for company name: {company_name}")
            return None, None, []

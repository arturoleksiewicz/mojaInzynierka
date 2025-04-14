import pandas as pd
import yfinance as yf
from fuzzywuzzy import process


class YahooFinanceFetcher:
    def __init__(self, file_path):
        # Wczytanie danych z pliku CSV
        self.company_data = pd.read_csv(file_path)
        # Zakładamy, że w pliku CSV znajdują się kolumny "Name" i "Symbol"
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

                # Format danych do listy słowników, do której dołączone są daty
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


# Blok testowy dla szybkiego sprawdzenia działania klasy
if __name__ == "__main__":
    # Ustaw właściwą ścieżkę do pliku CSV zawierającego kolumny "Name" i "Symbol"
    file_path = "nasdaqList.csv"
    try:
        fetcher = YahooFinanceFetcher(file_path)
    except Exception as e:
        print(f"Nie udało się wczytać pliku CSV: {e}")
        exit(1)

    company_name = input("Podaj nazwę firmy do wyszukania: ").strip()
    if not company_name:
        print("Nie podano nazwy firmy.")
    else:
        matched_name, ticker, stock_data = fetcher.fetch_stock_data(company_name)

        if matched_name is not None:
            print(f"\nNajlepsze dopasowanie: {matched_name} (Ticker: {ticker})")
            if stock_data:
                print("\nPrzykładowe dane o akcjach:")
                # Konwertujemy dane do DataFrame i wyświetlamy kilka pierwszych wierszy
                stock_df = pd.DataFrame(stock_data)
                print(stock_df.head())
            else:
                print("Brak danych o akcjach.")
        else:
            print("Nie znaleziono dopasowania.")

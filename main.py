from company_info_fetcher import CompanyInfoFetcher
from linkedin_formatter import display_linkedin_data

def display_company_info(company_info):
    for key, value in company_info.items():
        if key == "News Data":
            print("\n=== News Data ===")
            for title, content, summary, polarity, subjectivity in value:
                print(f"Title: {title}")
                print(f"Content: {content}")
                print(f"Summary: {summary}")
                print(f"Sentiment Polarity: {polarity}")
                print(f"Sentiment Subjectivity: {subjectivity}\n")
        elif key == "LinkedIn Data":
            print("\n=== LinkedIn Data ===")
            display_linkedin_data(value)
        elif key == "Yahoo Finance Data":
            print("\n=== Yahoo Finance Data ===")
            matched_name = value.get("Matched Company Name", "N/A")
            ticker_symbol = value.get("Ticker Symbol", "N/A")
            stock_data = value.get("Stock Data", "No stock data available.")
            print(f"Matched Company Name: {matched_name}")
            print(f"Ticker Symbol: {ticker_symbol}")
            print(f"Stock Data:\n{stock_data}")
        elif key == "Google Search Results":
            print("\n=== Google Search Results ===")
            for result in value:
                print(result)
        elif key == "Google Trends Image":
            print("\n=== Google Trends Image ===")
            print(f"Image saved at: {value}")
        else:
            print(f"\n=== {key} ===")
            print(value)

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    fetcher = CompanyInfoFetcher(company_name)
    company_info = fetcher.fetch_all_info()
    display_company_info(company_info)

import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import time
from requests.exceptions import HTTPError

class GoogleTrendsFetcher:
    def fetch_google_trends(self, keyword):
        pytrends = TrendReq(hl='en-US', tz=360)
        retries = 5
        for attempt in range(retries):
            try:
                pytrends.build_payload([keyword], cat=0, timeframe='today 12-m')
                data = pytrends.interest_over_time().reset_index()

                # Plot the data
                plt.figure(figsize=(10, 6))
                plt.plot(data['date'], data[keyword], label=keyword)
                plt.title('Keyword Web Search Interest Over Time')
                plt.xlabel('Date')
                plt.ylabel('Interest')
                plt.legend()
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Save the figure
                output_path = f'static/{keyword}_interest_over_time.png'
                plt.savefig(output_path)
                return output_path
            except HTTPError as e:  # Catch HTTP errors like TooManyRequests
                print(f"HTTP Error (e.g., TooManyRequests) on attempt {attempt + 1}: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None

        print("Failed to fetch Google Trends data after several attempts.")
        return None

# Example usage
if __name__ == "__main__":
    fetcher = GoogleTrendsFetcher()
    result = fetcher.fetch_google_trends("Python")
    if result:
        print(f"Image saved to {result}")
    else:
        print("Failed to fetch trends.")

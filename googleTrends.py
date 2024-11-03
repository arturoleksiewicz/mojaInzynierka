import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import time

class GoogleTrendsFetcher:
    def fetch_google_trends(self, keyword):
        pytrends = TrendReq(hl='en-US', tz=360)
        retries = 5
        for attempt in range(retries):
            try:
                pytrends.build_payload([keyword], cat=0, timeframe='today 12-m')
                data = pytrends.interest_over_time().reset_index()

                plt.figure(figsize=(10, 6))
                plt.plot(data['date'], data[keyword], label=keyword)
                plt.title('Keyword Web Search Interest Over Time')
                plt.xlabel('Date')
                plt.ylabel('Interest')
                plt.legend()
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                output_path = f'static/{keyword}_interest_over_time.png'
                plt.savefig(output_path)
                plt.show()
                return output_path
            except pytrends.exceptions.TooManyRequestsError:
                print(f"Too many requests error on attempt {attempt + 1}. Retrying after delay...")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None

        print("Failed to fetch Google Trends data after several attempts.")
        return None

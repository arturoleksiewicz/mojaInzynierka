import requests
import json
from bs4 import BeautifulSoup
import os

class TrustpilotFetcher:
    def __init__(self, serpapi_api_key=None):
        if serpapi_api_key is None:
            serpapi_api_key = os.getenv("serpapi")
        self.serpapi_api_key = serpapi_api_key

    def search_trustpilot(self, company_name):
        query = f"{company_name} site:trustpilot.com"
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_api_key,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return f"Failed to retrieve search results. Status code: {response.status_code}"

        data = response.json()
        search_results = []
        organic_results = data.get("organic_results", [])
        for result in organic_results:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                search_results.append((title, link))

        detailed_results = []
        for title, link in search_results:
            print(f"Pobieranie danych z Trustpilot: {link}")
            reviews_data = self.fetch_reviews_data(link)
            detailed_results.append((title, link, reviews_data))

        return detailed_results

    def fetch_reviews_data(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return {"review_count": "N/A", "average_score": "N/A"}

            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find("script", type="application/ld+json")
            if script_tag:
                data = json.loads(script_tag.string)
                if '@graph' in data:
                    for item in data['@graph']:
                        if item.get('@type') == 'LocalBusiness' and 'aggregateRating' in item:
                            rating_data = item['aggregateRating']
                            return {
                                "review_count": rating_data.get("reviewCount", "N/A"),
                                "average_score": rating_data.get("ratingValue", "N/A"),
                            }
            return {"review_count": "N/A", "average_score": "N/A"}
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return {"review_count": "N/A", "average_score": "N/A"}


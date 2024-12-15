import requests
import os
import json
from bs4 import BeautifulSoup


class TrustpilotFetcher:
    def search_trustpilot(self, company_name):
        query = f"{company_name} site:trustpilot.com"
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Failed to retrieve search results. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        for g in soup.find_all('div', class_='g'):
            title = g.find('h3')
            if title:
                title_text = title.get_text()
                link = g.find('a')['href']
                search_results.append((title_text, link))

        detailed_results = []
        for title, link in search_results:
            reviews_data = self.fetch_reviews_data(link, headers)
            detailed_results.append((title, link, reviews_data))

        return detailed_results

    def fetch_reviews_data(self, url, headers):
        """
        Fetch review count and average score from a Trustpilot page using JSON-LD.
        """
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return {"review_count": "N/A", "average_score": "N/A"}

            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find("script", type="application/ld+json")

            if script_tag:
                data = json.loads(script_tag.string)

                # Traverse JSON-LD for aggregateRating
                if '@graph' in data:
                    for item in data['@graph']:
                        if item.get('@type') == 'LocalBusiness' and 'aggregateRating' in item:
                            rating_data = item['aggregateRating']
                            return {
                                'review_count': rating_data.get("reviewCount", "N/A"),
                                'average_score': rating_data.get("ratingValue", "N/A"),
                            }

            return {"review_count": "N/A", "average_score": "N/A"}

        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return {"review_count": "N/A", "average_score": "N/A"}


# Usage within the application
if __name__ == "__main__":
    trustpilot_fetcher = TrustpilotFetcher()
    company_name = "Panasonic"
    results = trustpilot_fetcher.search_trustpilot(company_name)

    for title, link, reviews_data in results:
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Review Count: {reviews_data['review_count']}")
        print(f"Average Score: {reviews_data['average_score']}\n")

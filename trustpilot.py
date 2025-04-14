import requests
import json
from bs4 import BeautifulSoup


class TrustpilotFetcher:
    def __init__(self, serpapi_api_key="e4017084ad01edc1cad1f43656c4551b6723ef1e76f6cb6e208cd7d0a2291587"):
        # Ustaw domyślny klucz API, jeśli nie został przekazany
        if serpapi_api_key is None:
            # Podmień poniżej na swój klucz API lub użyj zmiennej środowiskowej
            serpapi_api_key = "<YOUR_SERPAPI_API_KEY>"
        self.serpapi_api_key = serpapi_api_key

    def search_trustpilot(self, company_name):
        # Budujemy zapytanie z ograniczeniem do trustpilot.com
        query = f"{company_name} site:trustpilot.com"
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_api_key,
            # Opcjonalnie można dodać np. "hl": "pl" dla polskich wyników
        }
        # Wysyłamy zapytanie do SerpApi
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return f"Failed to retrieve search results. Status code: {response.status_code}"

        data = response.json()
        # Wyniki organiczne SerpApi znajdują się w polu "organic_results"
        search_results = []
        organic_results = data.get("organic_results", [])
        for result in organic_results:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                search_results.append((title, link))

        detailed_results = []
        # Dla każdego wyniku pobieramy informacje o recenzjach
        for title, link in search_results:
            print(f"Pobieranie danych z Trustpilot: {link}")
            reviews_data = self.fetch_reviews_data(link)
            detailed_results.append((title, link, reviews_data))

        return detailed_results

    def fetch_reviews_data(self, url):
        """
        Pobiera liczbę recenzji i średnią ocenę ze strony Trustpilot na podstawie danych JSON-LD.
        """
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
                # Jeśli dane występują w polu '@graph', przeszukujemy je pod kątem aggregateRating
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


# Przykładowe wywołanie klasy
if __name__ == "__main__":
    # Tworzymy obiekt bez konieczności przekazywania klucza API (użyje się domyślnej wartości)
    trustpilot_fetcher = TrustpilotFetcher()
    company_name = input("Podaj nazwę firmy do wyszukania na Trustpilot: ").strip()
    if not company_name:
        print("Nie podano nazwy firmy.")
    else:
        results = trustpilot_fetcher.search_trustpilot(company_name)
        # Jeśli wynikiem jest komunikat o błędzie (str), wypisz go
        if isinstance(results, str):
            print(results)
        else:
            for title, link, reviews_data in results:
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Review Count: {reviews_data['review_count']}")
                print(f"Average Score: {reviews_data['average_score']}\n")

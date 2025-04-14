import requests
from bs4 import BeautifulSoup


class StatistaFetcher:
    def __init__(self, serpapi_api_key="e4017084ad01edc1cad1f43656c4551b6723ef1e76f6cb6e208cd7d0a2291587"):
        # Ustawiamy domyślny klucz API, jeśli nie został podany
        if serpapi_api_key is None:
            # Możesz tutaj wprowadzić swój klucz API lub odczytać ze zmiennej środowiskowej,
            # np.: serpapi_api_key = os.getenv("SERPAPI_API_KEY")
            serpapi_api_key = "<YOUR_SERPAPI_API_KEY>"
        self.serpapi_api_key = serpapi_api_key

    def search_statista(self, company_name):
        # Budujemy zapytanie z ograniczeniem do statista.com
        query = f"{company_name} site:statista.com"
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_api_key
            # Opcjonalnie można dodać np. "hl": "pl" dla wyszukiwania w języku polskim
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return f"Failed to retrieve search results. Status code: {response.status_code}"

        data = response.json()
        # Wyniki organiczne z SerpApi są przechowywane w polu "organic_results"
        search_results = []
        organic_results = data.get("organic_results", [])
        for result in organic_results:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                search_results.append((title, link))

        detailed_results = []
        for title, link in search_results:
            print(f"Pobieranie zawartości: {link}")
            page_content = self.fetch_page_content(link)
            detailed_results.append((title, link, page_content))

        return detailed_results

    def fetch_page_content(self, url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return f"Failed to retrieve page content. Status code: {response.status_code}"
            page_soup = BeautifulSoup(response.text, 'html.parser')
            for img in page_soup.find_all('img'):
                img.decompose()
            content = page_soup.get_text(separator="\n", strip=True)
            stop_phrase = "Skip to main content"
            if stop_phrase in content:
                content = content.split(stop_phrase)[0]
            return content
        except Exception as e:
            return f"An error occurred: {e}"

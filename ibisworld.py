from serpapi import GoogleSearch

class IbisWorldFetcher:
    def __init__(self, serp_api_key):
        self.serp_api_key = serp_api_key

    def search_ibisworld(self, company_name):
        # Tworzenie linku i tytułu do Crunchbase
        crunchbase_link = f"https://www.crunchbase.com/organization/{company_name.replace(' ', '-').lower()}"
        crunchbase_title = f"Crunchbase - {company_name}"

        # Wykorzystanie SERP API do wyszukiwania Google
        query = f"{company_name} site:ibisworld.com"
        retries = 3
        for _ in range(retries):
            try:
                search = GoogleSearch({
                    "q": query,
                    "api_key": self.serp_api_key
                })
                results = search.get_dict()
                organic_results = results.get("organic_results", [])

                # Parsowanie wyników z SERP API
                search_results = []
                for result in organic_results:
                    title = result.get('title', 'No Title')
                    link = result.get('link', 'No Link')
                    search_results.append((title, link))

                # Zwrócenie listy z Crunchbase jako pierwszym elementem
                return [(crunchbase_title, crunchbase_link)] + search_results
            except Exception as e:
                print(f"Search failed: {e}")

        return [(crunchbase_title, crunchbase_link)]
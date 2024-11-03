from serpapi import GoogleSearch

class GoogleSearchFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def google_search(self, query):
        retries = 3
        for _ in range(retries):
            try:
                search = GoogleSearch({
                    "q": query,
                    "api_key": self.api_key
                })
                results = search.get_dict()
                return results.get("organic_results", [])
            except Exception as e:
                print(f"Search failed: {e}")
        return []

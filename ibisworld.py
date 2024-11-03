import requests
from bs4 import BeautifulSoup

class IbisWorldFetcher:
    def search_ibisworld(self, company_name):
        query = f"{company_name} site:ibisworld.com"
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

        return search_results

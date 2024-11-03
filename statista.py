import requests
from bs4 import BeautifulSoup

class StatistaFetcher:
    def search_statista(self, company_name):
        query = f"{company_name} site:statista.com"
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
            page_content = self.fetch_page_content(link, headers)
            detailed_results.append((title, link, page_content))

        return detailed_results

    def fetch_page_content(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
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

